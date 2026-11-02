# mathkg

## Email (Brevo)

Railway blocks outbound SMTP. Activation mail, password reset, and the
new-subscription notice are sent with Brevo's transactional HTTP API
(`POST https://api.brevo.com/v3/smtp/email`, 10 second timeout) from
`MathKG <mathematicskgz@gmail.com>`.

Set this on the Railway service (Variables):

```
BREVO_API_KEY=
```

The key is created in Brevo under SMTP & API → API keys. The sender
address must be a verified sender in that Brevo account. See
`.env.example`. If `BREVO_API_KEY` is empty, Django prints mail to the
console instead. A failed send is logged and does not fail registration.