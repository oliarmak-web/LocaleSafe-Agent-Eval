# Security

Scoring runs locally. The service simulator changes in-memory state; the optional order controls write local SQLite databases. Neither contacts external services, dispatches help, sends messages or changes real bookings or orders.

No keys are needed. Keep credentials, private conversations, model weights, and environments out of Git. Future provider credentials belong only in backend processes. Rotate exposed keys; ignoring a file does not erase history.

The optional collector downloads pinned public weights, requires safetensors, and disables remote model code. Use a virtual environment and trusted registries. Review artifacts before sharing. Resource limits for untrusted hosted use are not implemented.

No public UI is launched. The old Colab Gradio demo enabled public sharing; do not copy that deployment behavior by default.

Report vulnerabilities privately through GitHub reporting if enabled; otherwise request a private channel without posting secrets or exploit details.
