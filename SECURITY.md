# Security

The evaluator runs offline and does not execute supplied tool calls, import plugins from artifacts, evaluate code strings, or contact model providers. Inputs and reports are plain JSON. Treat untrusted files as untrusted data and run with ordinary user permissions. File size/resource limits and hosted-service hardening are not implemented; this is a local research CLI.

No credentials are needed. Never commit `.env` files, provider keys, personal data, raw sensitive conversations, notebook secrets, or credential-bearing outputs. Future integrations must load secrets only in server-side processes and keep credentials out of responses, error messages, browser bundles, and version control. Ignoring a file does not remove an already committed secret: revoke exposed credentials and inspect history.

The original Colab demo's Gradio launch automatically enabled public sharing. This release does not launch a web service. Any future UI should default to local access; public sharing must be an explicit deployment choice with authentication, rate limits, dependency review, and data handling documented.

Report suspected security issues privately using GitHub private vulnerability reporting if enabled; otherwise request a private contact channel without posting exploit details or credentials. Private vulnerability reporting still needs to be enabled by the repository owner before public release.
