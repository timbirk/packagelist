# packagelist
Script that returns a list of packages suitable for use with yum or other package managers.

## Why?
When deploying to different environments, server roles, versions, sometimes we need different sets of packages. Some `test` package in non-prod, some new service on version x. This script and config allows you to do that. 

## How
```
$ python packagelist.py -h
usage: packagelist.py [-h] -r ROLE [-e ENV] [-x] [-v VERSION] [-f CONFIG]

Lists packages for the target role / environment.

optional arguments:
  -h, --help            show this help message and exit
  -r ROLE, --role ROLE  role to target
  -e ENV, --env ENV     environment to target
  -x, --exclude         output excluded packages
  -v VERSION, --version VERSION
                        package version
  -f CONFIG, --config CONFIG
                        configuration file
 ```
 
 Example config:
 ```
 ---
account_services:
  include:
    - talpay-account-ibusiness
    - talpay-account-reconnet
    - talpay-test-ibusiness
    - talpay-test-reconnet
    - talpay-test-ftp-server
  environments:
    pre:
      exclude:
        - talpay-test-ibusiness
        - talpay-test-reconnet
        - talpay-test-ftp-server
    prod:
      exclude:
        - talpay-test-ibusiness
        - talpay-test-reconnet
        - talpay-test-ftp-server

data_services:
  include:
    - talpay-data-user
    - talpay-data-party
    - talpay-data-payment

exchange_services:
  include:
    - talpay-ibusiness-epayment
    - talpay-ibusiness-ledger
    - talpay-dbextract
    - talpay-extract-gtvap
    - talpay-export-gtvap

payment_services:
  include:
    - talpay-payment-calculator
    - talpay-payment-epayment
    - talpay-payment-print-service
    - talpay-test-cheque-printer
  environments:
    pre:
      exclude:
        - talpay-test-cheque-printer
    prod:
      exclude:
        - talpay-test-cheque-printer

user_services:
  include:
    - talpay-user-authorisation
    - talpay-user-express-pay
    - talpay-user-home
    - talpay-user-party
    - talpay-user-payment
    - talpay-user-permission
    - talpay-user-prize
    - talpay-user-refund
    - talpay-user-static
    - talpay-test-oauth2-server
    - talpay-test-webapp
  versions:
    6.2:
      include:
        - talpay-user-pcs
        - talpay-test-pcs
        - talpay-user-secondary
  environments:
    pre:
      exclude:
        - talpay-test-oauth2-server
        - talpay-test-webapp
        - talpay-test-pcs
    prod:
      exclude:
        - talpay-test-oauth2-server
        - talpay-test-webapp
        - talpay-test-pcs

workflow_services:
  include:
    - talpay-framework-action
    - talpay-framework-audit
    - talpay-framework-notification
    - talpay-framework-reports
    - talpay-framework-scheduling
    - talpay-framework-workflow
    - talpay-test-email-server
  environments:
    pre:
      exclude:
        - talpay-test-email-server
    prod:
      exclude:
        - talpay-test-email-server
```

You can see I have serveral roles: `user_services`, `workflow_services` etc. Example for `user_services`: 
```
user_services:
  include:
    - talpay-user-authorisation
    - talpay-user-express-pay
    - talpay-user-home
    - talpay-user-party
    - talpay-user-payment
    - talpay-user-permission
    - talpay-user-prize
    - talpay-user-refund
    - talpay-user-static
    - talpay-test-oauth2-server
    - talpay-test-webapp
  versions:
    6.2:
      include:
        - talpay-user-pcs
        - talpay-test-pcs
        - talpay-user-secondary
  environments:
    pre:
      exclude:
        - talpay-test-oauth2-server
        - talpay-test-webapp
        - talpay-test-pcs
    prod:
      exclude:
        - talpay-test-oauth2-server
        - talpay-test-webapp
        - talpay-test-pcs
```
From this config hash we can see a set of package names under the main role `include`, Then we say "for versions starting with `6.2`, include these other packages". On the `pre` and `prod` environments we want to exclude a few test packages.

The resulting output for a version of: `6.1.0-5` on the `qa1` environment is:
```
$ python packagelist.py -f packagelist.yaml  -r user_services -e qa1 -v 6.1.0-5
talpay-test-oauth2-server-6.1.0-5 talpay-test-webapp-6.1.0-5 talpay-user-authorisation-6.1.0-5 talpay-user-express-pay-6.1.0-5 talpay-user-home-6.1.0-5 talpay-user-party-6.1.0-5 talpay-user-payment-6.1.0-5 talpay-user-permission-6.1.0-5 talpay-user-prize-6.1.0-5 talpay-user-refund-6.1.0-5 talpay-user-static-6.1.0-5
```

For version `6.2.3-1` on the `pre` environment:
```
$ python packagelist.py -f packagelist.yaml  -r user_services -e pre -v 6.2.3-1
talpay-user-authorisation-6.2.3-1 talpay-user-express-pay-6.2.3-1 talpay-user-home-6.2.3-1 talpay-user-party-6.2.3-1 talpay-user-payment-6.2.3-1 talpay-user-pcs-6.2.3-1 talpay-user-permission-6.2.3-1 talpay-user-prize-6.2.3-1 talpay-user-refund-6.2.3-1 talpay-user-secondary-6.2.3-1 talpay-user-static-6.2.3-1
```

We can see what is excuded from a role / environment with the `-x` flag which is useful for testing configuration:
```
$ python packagelist.py -f packagelist.yaml  -r user_services -e qa1 -x

$ python packagelist.py -f packagelist.yaml  -r user_services -e pre -x
talpay-test-oauth2-server talpay-test-pcs talpay-test-webapp
```

> Note about versioning: No assumptions are made about your versioning, we simply cast the version to a string and check if the version passed to the script starts with the version string in the config so you would need to update your config for version `6.3` to include anything required from version `6.2` configuration. Ideally you'd be moving packages into the main `include` config when they are ready and getting rid of version specific config as soon as you can. 
