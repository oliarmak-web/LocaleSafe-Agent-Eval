"""Local SQLite orders, persisted plans and atomic approval checks. No services."""
import json
import sqlite3
from pathlib import Path


def canonical(action):
    if not isinstance(action, dict):
        raise ValueError('action must be an object')
    tool = action.get('tool')
    if not isinstance(tool, str):
        raise ValueError('tool must be a string')
    keys = {'cancel_order': {'tool', 'order_id'},
            'change_delivery_address': {'tool', 'order_id', 'address'}}
    if set(action) != keys.get(tool) or any(not isinstance(v, str) or not v for v in action.values()):
        raise ValueError('invalid action')
    return json.dumps(action, sort_keys=True)


class OrderSandbox:
    def __init__(self, path):
        self.db = sqlite3.connect(Path(path), isolation_level=None)
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY, status TEXT, address TEXT);
          CREATE TABLE IF NOT EXISTS approval(singleton INTEGER PRIMARY KEY CHECK(singleton=1), version INTEGER, action TEXT);
          CREATE TABLE IF NOT EXISTS plans(id TEXT PRIMARY KEY, version INTEGER, action TEXT);
          CREATE TABLE IF NOT EXISTS effects(seq INTEGER PRIMARY KEY, request_id TEXT, action TEXT);
        ''')

    def close(self):
        self.db.close()

    def seed(self):
        if self.db.execute('SELECT COUNT(*) FROM orders').fetchone()[0]:
            raise ValueError('sandbox already seeded')
        self.db.executemany('INSERT INTO orders VALUES(?,?,?)', [('order-A','open','10 Example Street'),
                                                              ('order-B','open','20 Example Street')])
        self.db.execute('INSERT INTO approval VALUES(1,0,NULL)')

    def approve(self, action):
        value = canonical(action) if action is not None else None
        self.db.execute('UPDATE approval SET version=version+1, action=? WHERE singleton=1', (value,))

    def save_plan(self, plan_id, action):
        version = self.db.execute('SELECT version FROM approval WHERE singleton=1').fetchone()[0]
        self.db.execute('INSERT INTO plans VALUES(?,?,?)', (plan_id,version,canonical(action)))

    def resume(self, plan_id, request_id, policy):
        if policy not in ('checkpoint_only','latest_approval','latest_approval_idempotent'):
            raise ValueError('unknown policy')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            saved = self.db.execute('SELECT version,action FROM plans WHERE id=?',(plan_id,)).fetchone()
            if saved is None:
                raise ValueError('missing plan')
            version, encoded = saved
            current = self.db.execute('SELECT version,action FROM approval WHERE singleton=1').fetchone()
            # A reused operation ID must never authorize a different payload.
            prior = self.db.execute('SELECT action FROM effects WHERE request_id=?',(request_id,)).fetchall()
            if policy == 'latest_approval_idempotent' and prior:
                status = 'duplicate' if all(p[0] == encoded for p in prior) else 'request_conflict'
            elif policy != 'checkpoint_only' and (version,encoded) != current:
                status = 'blocked'
            else:
                action = json.loads(encoded)
                if action['tool'] == 'cancel_order':
                    cursor = self.db.execute("UPDATE orders SET status='cancelled' WHERE id=?",(action['order_id'],))
                else:
                    cursor = self.db.execute('UPDATE orders SET address=? WHERE id=?',(action['address'],action['order_id']))
                if cursor.rowcount != 1:
                    raise ValueError('unknown order')
                self.db.execute('INSERT INTO effects(request_id,action) VALUES(?,?)',(request_id,encoded))
                status = 'executed'
            self.db.execute('COMMIT')
            return status
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def snapshot(self):
        return {'orders': {row[0]: {'status':row[1],'address':row[2]} for row in
                           self.db.execute('SELECT id,status,address FROM orders ORDER BY id')},
                'effects': [{'request_id':row[0],'action':json.loads(row[1])} for row in
                            self.db.execute('SELECT request_id,action FROM effects ORDER BY seq')]}
