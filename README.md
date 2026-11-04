# mathkg

## Email (Brevo)

Railway blocks outbound SMTP. Activation mail, password reset, and the
new-subscription notice are sent with Brevo's transactional HTTP API
(`POST https://api.brevo.com/v3/smtp/email`, 10 second timeout) from
`MathKG <no-reply@mathkg.com>`.

Set this on the Railway service (Variables):

```
BREVO_API_KEY=
```

The key is created in Brevo under SMTP & API → API keys. The sender
domain must be authenticated in that Brevo account. The address defaults
to `no-reply@mathkg.com` and can be overridden with `BREVO_SENDER_EMAIL`
or `DEFAULT_FROM_EMAIL` (the full header wins). Replies go to
`mathematicskgz@gmail.com` (`DEFAULT_REPLY_TO_EMAIL`). See
`.env.example`. If `BREVO_API_KEY` is empty, Django prints mail to the
console instead. A failed send is logged and does not fail registration.