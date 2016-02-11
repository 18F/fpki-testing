# FPKI Testing

Testing out Federal PKI certificate chains.

The certificate being used for testing is valid for 15 SANs: `test[1..15].fpki.18f.gov` and can be found at [`18f-fpki-testing.crt`](chains/18f-fpki-testing.crt).

## Certificate chains

* [`test1`](https://test1.fpki.18f.gov) - No intermediates, end entity certificate only.

* [`test2`](https://test2.fpki.18f.gov) - Intermediate chain up to `Federal Bridge CA 2013`.
  * https://crt.sh/?id=8764555
  * https://crt.sh/?id=3264194
  * https://crt.sh/?id=2981779
  * https://crt.sh/?id=12638543

* [`test3`](https://test3.fpki.18f.gov) - Intermediate chain up to Identrust's `DST ACES CA X6`.

* [`test4`](https://test4.fpki.18f.gov) - Intermediate chain up to Symantec's `VeriSign Universal Root Certification Authority`.

See [`chains/`](chains/) for constructed certificate chains for each host.

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
