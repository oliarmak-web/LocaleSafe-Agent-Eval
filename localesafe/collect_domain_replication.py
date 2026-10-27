"""Run the unchanged domain collector with the pinned Phi replication."""
from . import collect_domain_study as collector
from .collect_handoff import MODELS

EXTRA_SOURCES=('localesafe/collect_domain_replication.py','experiments/domain-study/MODEL_REPLICATION.md')


def main():
    collector.MODELS={'phi4-mini':MODELS['phi4-mini']}
    collector.SOURCES=(*collector.SOURCES,*EXTRA_SOURCES)
    collector.main()


if __name__=='__main__':main()
