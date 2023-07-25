#!/usr/bin/guile
!#

(define hypotinuse
  (lambda(a b)
    (sqrt (+(* a a) (* b b)))
    )
)

(define ssdexp
  (lambda (number the_mult)
    (if (= number 0)
      0 
      (if (> the_mult 0)
        (* number (ssdexp number (- the_mult 1)))
        1 
      )
    )
  )
)

(define bye "Kwa heri unnecessarily cruel world!")
(display bye)
(newline)
(display (hypotinuse 2 6))
(newline)

(define fact_r
  (lambda (number)
    (if (= number 1)
      1
      (* number (fact_r (- number 1)))
    )
  )
)

(display (fact_r 10))
(newline)
(display (ssdexp -4 3))
(newline)
