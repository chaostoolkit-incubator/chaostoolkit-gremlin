# chaostoolkit-gremlin

[![Build Status](https://travis-ci.org/chaostoolkit/chaostoolkit-gremlin.svg?branch=master)](https://travis-ci.org/chaostoolkit/chaostoolkit-gremlin)

[Gremlin, Inc][gremlin] support for the [Chaos Toolkit][chaostoolkit].

[gremlin]: https://www.gremlin.com/
[chaostoolkit]: http://chaostoolkit.org/

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install chaostoolkit-gremlin
```

## Usage

To use this package, you must create an account with [Gremlin, Inc][gremlin].
Once registered, create a new organization (formerly known as team). You may
have to ask your Gremlin administrator to do this for you.

Once this is done, you must set the following environmental variables
so the Chaos Toolkit can pick up them:

* `GREMLIN_EMAIL`: the email used to register to Gremlin and associated to that
  organization
* `GREMLIN_PWD`: your password
* `GREMLIN_ORG_NAME`: the organization's name you created

Note that 2FA is not yet implemented in this package.

Next you need to specify to load those
variables and inject them into this package's activities. At the top of the
experiment file, add the following object:

```json
{
    "secrets": {
        "gremlin": {
            "email": {
                "type": "env",
                "key": "GREMLIN_EMAIL"
            },
            "password": {
                "type": "env",
                "key": "GREMLIN_PWD"
            },
            "org_name": {
                "type": "env",
                "key": "GREMLIN_ORG_NAME"
            }
        }
    }
}
```

Finally, in all activities where you call a function from this package, make
sure to add the following property:

```json
"secrets": ["gremlin"]
```

Here is a full example of running a CPU attack experiment:

```json
{
    "title": "Can our system handle a node being CPU-busy?",
    "description": "CPU-usage may be impactful on our response time",
    "secrets": {
        "gremlin": {
            "email": {
                "type": "env",
                "key": "GREMLIN_EMAIL"
            },
            "password": {
                "type": "env",
                "key": "GREMLIN_PWD"
            },
            "org_name": {
                "type": "env",
                "key": "GREMLIN_ORG_NAME"
            }
        }
    },
    "method": [
        {
            "name": "attack-on-cpu",
            "type": "action",
            "background": true,
            "provider": {
                "type": "python",
                "module": "chaosgremlin.actions",
                "func": "attack",
                "secrets": ["gremlin"],
                "arguments": {
                    "command": {
                        "type": "cpu"
                    },
                    "target": {
                        "type": "Random"
                    }
                }
            }
        }
    ]
}
```

### API Key Authentication

In order to use an API Key as your method of authentication, you'll have to set it as an environment variable: `$GREMLIN_API_KEY`.
You can construct your experiments the same as before, but with the `secrets` section omitted. When `secrets` is not present, chaostoolkit-gremlin will grab your pre-registered Gremlin API Key and bundle it with your experiment at runtime. 
Here's an example of the above CPU attack, with API Key authentication:
```json
{
    "title": "Can our system handle a node being CPU-busy?",
    "description": "CPU-usage may be impactful on our response time",
    "method": [
        {
            "name": "attack-on-cpu",
            "type": "action",
            "background": true,
            "provider": {
                "type": "python",
                "module": "chaosgremlin.actions",
                "func": "attack",
                "arguments": {
                    "command": {
                        "type": "cpu"
                    },
                    "target": {
                        "type": "Random"
                    }
                }
            }
        }
    ]
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/
