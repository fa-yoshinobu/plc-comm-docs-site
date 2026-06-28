# License, Commercial Support, and Sponsorship

This page explains the license model for the PLC communication libraries and
how commercial users can support continued maintenance.

## License

The PLC communication libraries are published as open source software. Unless a
specific repository says otherwise, the libraries use the MIT License.

The MIT License allows broad use, including:

- using the library in private or commercial projects
- embedding the library in paid products
- modifying the source code for your own application
- redistributing the library or derived works

When redistributing the software, keep the copyright notice and license text
included with the relevant repository.

The libraries are provided without warranty. Please review the `LICENSE` file in
each source repository before shipping a product that depends on the library.

## Commercial Support

If you plan to embed this library in a paid or commercial product, please
consider a separate support agreement or supporting the project as a sponsor.

Commercial support can help with:

- implementation review before deployment
- PLC connection and profile selection guidance
- troubleshooting communication errors
- priority investigation for production issues
- custom validation against specific PLC models
- documentation or sample improvements for your use case

Contact: [https://fa-labo.com/contact.html](https://fa-labo.com/contact.html)

## Sponsorship and Donations

These libraries are maintained to make PLC communication easier and safer for
developers. Sponsorship and donations help cover maintenance time, test
hardware, documentation work, and continued compatibility checks across .NET,
Python, Rust, C++, and Node-RED implementations.

Please consider supporting the project if the libraries save development time,
reduce integration risk, or are used in a commercial environment.

Ways to support the project include:

- arranging a commercial support agreement
- sponsoring continued development
- funding validation for a specific PLC model or protocol feature
- contributing fixes, documentation, or reproducible test cases
- sharing feedback about real-world usage and missing documentation

For sponsorship, donations, paid support, or custom work, please use the contact
page:

[https://fa-labo.com/contact.html](https://fa-labo.com/contact.html)

## Notes for Product Teams

Open source licensing and paid support are separate topics. The MIT License does
not require a paid agreement for commercial use, but a support agreement is
recommended when the library becomes part of a shipped product, production
system, or long-term maintenance plan.

Before release, product teams should confirm:

- the target repository license file is included where required
- PLC communication behavior has been validated with the actual target hardware
- application-level safety checks are in place for writes and remote operations
- maintenance ownership is clear for future PLC, firmware, runtime, or OS
  changes
