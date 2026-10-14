# Privacy Policy for linkedin_bot

**Effective date:** October 14, 2026  
**Last updated:** October 14, 2026

## Overview

`linkedin_bot` is a personal automation application operated by Omer Levy. It
uses OpenAI to generate DevOps and MLOps content and LinkedIn's official API to
publish that content to the operator's LinkedIn account.

The application is intended for use only by its operator. It is not offered as
a service to other LinkedIn members.

## Information the application processes

The application may process:

- A LinkedIn OAuth access token and LinkedIn member identifier required to
  publish posts on behalf of the operator.
- An OpenAI API key required to generate post content.
- Generated post text, publication timestamps, LinkedIn post identifiers, and
  short previews and cryptographic hashes of previously published posts.
- Technical logs related to successful or failed application runs.

The application does not intentionally collect LinkedIn passwords, contact
lists, private messages, or information belonging to other LinkedIn members.

## How information is used

Information is used only to:

- Generate educational DevOps and MLOps content.
- Publish generated content to the operator's LinkedIn account.
- Detect duplicate posts.
- Diagnose errors and maintain the application.

Personal information is not sold, rented, or used for advertising.

## Service providers

The application uses the following third-party services:

- **LinkedIn:** authenticates the operator and publishes posts through
  LinkedIn's API. LinkedIn processes information according to its own privacy
  policy and developer terms.
- **OpenAI:** receives prompts and related context needed to generate post
  content. OpenAI processes API data according to its applicable privacy and
  API data-usage policies.
- **GitHub:** hosts the application's source code and container images. Secrets
  are not intentionally stored in the source-code repository or container
  images.

## Storage and retention

API credentials are configured as secrets in the operator's private Kubernetes
environment. The application stores limited publication history on a private
persistent volume to reduce repeated content. Operational data is retained only
for as long as it remains useful for running and maintaining the application
and may be deleted by the operator at any time.

No method of storage or transmission is completely secure, but reasonable
technical measures are used to limit access, including secret separation,
least-privilege container settings, and restricted application access.

## Sharing and disclosure

Information is shared only with the service providers described above when
necessary to operate the application. Information may also be disclosed when
required by law or when reasonably necessary to protect the security and
integrity of the application.

## Your choices

The operator can stop the application, delete its stored history, rotate its
credentials, or revoke its LinkedIn authorization at any time through
LinkedIn's account settings. Because the application is not offered to other
users, it does not maintain accounts or personal profiles for the public.

## Changes to this policy

This policy may be updated when the application's behavior or service providers
change. Updates will be published in this repository with a revised
"Last updated" date.

## Contact

For questions about this policy or the application, contact Omer Levy through
the GitHub profile at <https://github.com/omerlevyk>.

