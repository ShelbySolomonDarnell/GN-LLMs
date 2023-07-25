(define-module (python_flask-minify)
  #:use-module (guix gexp)
  #:use-module (guix git-download)
  #:use-module (guix packages)
  #:use-module (guix download)
  #:use-module (guix build-system pyproject)
  #:use-module (guix build-system python)
  #:use-module (gnu packages python)
  #:use-module (gnu packages python-web)
  #:use-module (gnu packages python-xyz)
  #:use-module (gnu packages python-build)
  #:use-module (gnu packages digest)
  #:use-module ((guix licenses) #:prefix license:))

(define-public python-lesscpy
  (package
   (name "python-lesscpy")
   (version "0.15.1")
   (source (origin
            (method url-fetch)
            (uri (pypi-uri "lesscpy" version))
            (sha256
             (base32
              "0k42gjvw75833c41l1cfci2kgh79wrag5psqlxn6927nk1xd2i8h"))))
   (build-system pyproject-build-system)
   (arguments
    `(#:tests? #f))
   (propagated-inputs (list python-ply))
   (home-page "https://github.com/lesscpy/lesscpy")
   (synopsis "Python LESS compiler")
   (license license:expat)
   (description "Python LESS compiler")))

(define-public python-flask-minify
  (package
   (name "python-flask-minify")
   (version "0.42")
   (source (origin
            (method url-fetch)
            (uri (pypi-uri "Flask-Minify" version))
            (sha256
             (base32
              "12wcaclhd44bzwfypwsllkf4s9sjhj3hh2zxz6xhw85ljba9pbnd"))))
   (build-system python-build-system)
   (arguments
    `(#:tests? #f))
   (propagated-inputs (list python-flask
                            python-htmlmin
                            python-jsmin
                            python-lesscpy
                            python-rcssmin
                            python-six
                            python-xxhash))
   (home-page "https://github.com/mrf345/flask_minify/")
   (synopsis "Flask extension to minify html, css, js and less.")
   (description "Flask extension to minify html, css, js and less.")
   (license license:expat)))

(define %source-dir (dirname (current-filename)))

(package
 (name "genenetwork-qa")
 (version "0.1")
 (source (local-file %source-dir "gnqamatflask-checkout"
                     #:recursive? #t
                     #:select? (git-predicate
                                %source-dir)))
 (build-system pyproject-build-system)
 (arguments
  `(#:tests? #f))
 (propagated-inputs (list python
                          python-minimal-wrapper
                          python-flask
                          python-htmlmin
                          python-jsmin
                          python-lesscpy
                          python-rcssmin
                          python-flask-login
                          python-flask-migrate
                          python-wtforms
                          python-flask-wtf
                          python-flask-sqlalchemy
                          python-flask-migrate
                          python-email-validator
                          python-flask-minify
                          gunicorn
                          python-flask-restx
                          python-dotenv
                          python-six
                          python-xxhash))
 (home-page "https://github.com/ShelbySolomonDarnell/GN-LLMs/material-flask/")
 (synopsis "")
 (description "")
 (license license:expat))
