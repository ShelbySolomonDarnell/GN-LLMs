(define-module (ssd-so-long)
  #:use-module (guix licenses)
  #:use-module (guix packages)
  #:use-module (guix build-system gnu)
  #:use-module (guix download))

(define-public ssd-so-long
  (package
    (name "ssd-so-long")
    (version "2.10")
    (source (origin
              (method url-fetch)
              (uri (string-append "mirror://gnu/hello/hello-" version ".tar.gz"))
              (sha256
                (base32
                  "0ssi1wpaf7plaswqqjwigppsg5fyh99vdlb9kzl7c9lng89ndq1i"))))
    (build-system gnu-build-system)
    (synopsis "So long, Guix world: An example custom Guix package")
    (description "GNU solong prints the message \"So long cruel world!\" then exits. 
               As such, it supports command-line arguments, multiple languages and so on.")
    (home-page "https://www.nyeusi.tech/software/ssd-so-long/")
    (license gpl3+)))

ssd-so-long
