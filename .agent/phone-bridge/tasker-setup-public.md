# Odysseus Phone Bridge Tasker Setup via Cloudflare Tunnel

Tunnel URL: `https://comm-pages-profession-agents.trycloudflare.com/event`

The auth token is stored locally at:
`~/Library/Application Support/OdysseusPhoneBridge/tasker-setup-secure.txt`

Tasker action:
1. `Net -> HTTP Request`
2. Method: `POST`
3. URL: `https://comm-pages-profession-agents.trycloudflare.com/event`
4. Headers:
   - `Content-Type: application/json`
   - `X-Phone-Bridge-Token: <token from secure setup file>`
5. Body: use one JSON payload from the secure setup file.
