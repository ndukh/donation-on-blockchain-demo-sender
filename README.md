# TelegramSender

Telegram-bot interface, which allows to send a virtual donation to a random demo fund and get its ID.

It uses the [donation-on-blockhain-api](https://github.com/AplusD/dontation-on-blockchain-api)

### Deployment
Both modules are almost set up for deploying on IBM Bluemix CF (Python buildpack). Before deployment it is essential to:
- amend the parameters of `config_example.ini`;
- rename `config_example.ini` to `config.ini`;
- rename app in `manifest.yml`;
- *probably* make some other changes in [`manifest.yml`](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).
