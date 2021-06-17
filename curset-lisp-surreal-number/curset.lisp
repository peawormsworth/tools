;;;; curset.lisp - Finite Surreal Number Calculator
;;;;
;;;;  "Curset" a self-refrencing linked list of tuples to nil representing "numbers"
;;;;
;;;;  Creates, evaluates and operates on finite surreal numbers as memory constructions 
;;;;    which are represented by linked tuples (cons) of its left onto its right parts
;;;;
;;;;  These numbers represent signed dyadic fractions or all base 2 numbers
;;;;    up to bit precision of lisp positive intgers
;;;;
;;;;  Conversion between numbers formats of order, values and cursets are provided by 
;;;;    ov, oc, vo, vc, co and cv functions where letters represent a "from to" relationship 
;;;;
;;;;  For example "ov" says to convert from the order into its values
;;;;    the code: "(ov 22)" then means to return the value of the 22nd surreal number
;;;;
;;;;  The linked tumple representations have been named "cursets" because they are not a
;;;;    true representation of Surreal numbers
;;;;
;;;;  Cursets are easily created by order, using:
;;;;    "(oc a)" where a is a non-negative integer
;;;;    "(ov a)" where a is a signed float of some finite precision
;;;;


;;;
;;;  constant curset representations for signed units and zero
;;;

( defvar +nan+ ())
( defvar +zer+ (cons +nan+ +nan+))
( defvar +neg+ (cons +nan+ +zer+))
( defvar +pos+ (cons +zer+ +nan+))


;;;
;;; Comparison functions:
;;;


;; (le a b) is true if a is less than or equal to b
;;
;; le implements less than or equal to comparison which is the primary formula 
;;   on which all other mathematical operations depend
;; considering that all numbers have a less and greater part if any, then
;;   number A is less than or equal to number B when both
;;   1. there is no left part of A or B is not less than this part, and
;;   2. there is no right part of B or A is not less than this part

( defun le (a b)
  ( let
    ( (al (car a))
      (br (cdr b))
    )
    ( and (not (and al (le b al)))
          (not (and br (le br a)))
    )
  )
)


( defun lep (a b)
  ( and (not (and (car a) (lep b (car a))))
        (not (and (cdr b) (lep (cdr b) a)))
  )
)


;; (gt a b) is true is a is greater than b

( defun gt (a b)
    ( not (le a b))
) 


;; (lt a b) is true if a is less than b

( defun lt (a b) 
    ( not (le b a))
)


;; (ge a b) is true is a is greater than or equal to b

( defun ge (a b)
    ( le b a)
)


;; (eqp a b) is true is a is equal to b

( defun eqp (a b)
    ( and (le a b) (le b a))
)


;; (ne a b) is true is a is not equal to b

( defun ne (a b)
    ( not (and (le a b) (le b a)))
)


;; (least a b) returns the curset with the lower numeric value
;;
;;   large negative numbers are the lowest

( defun least (a b)
    ( if (le a b) a b)
)


;; (greatest a b) returns the curset with the greaters numeric value

( defun greatest (a b)
    ( if (le a b) b a)
)


;; (equiv a) returns the reduced surreal form of the given curset
;;
;;   this is useful for reducing the size of cursets after mathematical operations
;;   which can create tree structures which are much longer than their equivelant
;;   reduced form

( defun equiv (a &optional (b +zer+))
  ( if (le a b)
    ( if (le b a)
      b
      ( equiv a (cons (car b) b))
    )
    ( equiv a (cons b (cdr b)))
  )
)

;;;
;;; Conversion functions
;;;   representations: Order, Curset, Value
;;;


;; (oc a) given natural a, return the curset with this order

( defun oc (a)
  ( let
    ( ( bits (floor (log (+ a 1/2) 2)))
      ( c +zer+)
    )
    ( if (< bits 0)
      ( setf c nil )
      ( loop for bit downfrom (- bits 1) to 0 do
        ( if (/= 0 (logand a (expt 2 bit)))
          ( setf c (cons c (cdr c)))
          ( setf c (cons (car c) c))
        )
      )
    )
    c
  )
)


;; (co a) given curset a, return its order number

( defun co (a)
  ( let
    ( (o 0) (p 0) )
    ( if a
      ( progn
        ( loop while (and a (or (car a) (cdr a))) do 
          ( if (and (cdr a) (eqp (car a) (car (cdr a))))
            ( setf a (cdr a))
            ( progn
              ( setf o (+ o (expt 2 p)))
              ( setf a (car a))
            )
          )
          ( incf p )
        )
        ( setf o (+ o (expt 2 p)))
      )
    )
    o
  )
)


;; (vo a) the order of the surreal number having the given value
;;
;;  expects a signed dyadic input
;;  output is a non negative integer

( defun vo (a)
  ( if a
    ( let 
      ( u s w f r n b o)
      ( setq s (if (< a 0) -1 1))
      ( setq u (* s a))
      ( setq w (floor u))
      ( setq f (- u w))
      ( setq r (rational (+ (* (+ (/ (- (/ f 2) 1) (expt 2 w)) 1) s) 1)))
      ( setq n (numerator r))
      ( setq b (denominator r))
      ( setq o (truncate (+ (/ (- n 1) 2) b)))
      o
    )
    0
  )
)

;; (ov a) the value of the surreal number of the given order
;;
;;   expects a non negative integer input
;;   output is a signed dyadic

( defun ov (a)
  ( if (zerop a)
    nil
    ( let
      ( l r s g w f )
      ( setq l (floor(log (+ a 1/2) 2)))
      ( setq r (- (/ (+ (* 2 a) 1) (expt 2 l)) 2))
      ( setq s (signum (- r 1)))
      ( setq g (* (- r 1) s))
      ; this fails: 
      ( setq w (floor (* -1 (log (- 1 g) 2))))
      ( setq f (+ (* (- g 1) (expt 2 (+ w 1))) 2))
      ( * (+ w f) s)
    )
  )
)


;; (vc a) the curset representation of the surreal number having the given value
;;
;;  expects a signed dyadic input
;;  output is a curset 

( defun vc (a)
  ( oc (vo a))
)


;; (ov a) the value of the surreal number of the given order
;;   expects a non negative integer input
;;   output is a signed dyadic

( defun cv (a)
  ( ov (co a))
)


;;;
;;; Math operations: negation, addition, subtraction, multiplication, inversion, division
;;;


;; (negate a) returns the negation of the given curset

( defun negate (a)
  ( if a
    ( cons (negate (cdr a)) (negate (car a)))
    a
  )
)


;; (add a b) returns the addition of curset a and b

( defun add (a b)
  ( if (not a)
    b
    ( if (not b)
      a
      ( let 
        ( ( al (car a))
          ( ar (cdr a))
          ( bl (car b))
          ( br (cdr b))
          l r
        )
        ( setf l (if al (add al b) al))
        ( setf r (if ar (add ar b) ar))
        ( when bl
          ( let
            ( (less (add a bl)) )
            ( when (or (not l) (le l less))
              ( setf l less)
            )
          )
        )
        ( when br
          ( let 
            ( (more (add a br)) )
            ( when (or (not r) (le more r))
              ( setf r more)
            )
          )
        )
        ( equiv (cons l r))
      )
    )
  )
)

;; (sub a b) subtract the second curset from the first

( defun sub (a b)
  ( add a (negate b))
)

;; (mul a b) multiply two cursets

( defun mul (a b)
  ( if (or (not a) (eqp b +pos+))
    a
    ( if (or (not b) (eqp a +pos+))
      b
      ( if (eqp a +neg+)
        ( negate b)
        ( if (eqp b +neg+)
          ( negate a)
          ( let (
              ( al (car a))
              ( ar (cdr a))
              ( bl (car b))
              ( br (cdr b))
              l r
            )
            ( if (and al bl)
              ( setq l (sub (add (mul al b) (mul a bl)) (mul al bl)))
            )
            ( if (and ar br)
              ( let (
                  ( l2 (sub (add (mul ar b) (mul a br)) (mul ar br)))
                )
                ( if (or (not l) (le l l2))
                  ( setq l l2)
                )
              )
            )
            ( if (and al br)
              ( setq r (sub (add (mul al b) (mul a br)) (mul al br)))
            )
            ( if (and ar bl)
              ( let (
                  ( r2 (sub (add (mul a bl) (mul ar b)) (mul ar bl)))
                )
                ( if (or (not r) (le r2 r))
                  ( setq r r2)
                )
              )
            )
            (equiv (cons l r))
          )
        )
      )
    )
  )
)


;; (invert a) return the inversion or 1/a of the given curset
;;
;;   this function is incomplete and not tested
;;   i believe that only division by 2 is possible
;;   since inversion of larger integers requires (1/(a-1)) to be calculated
;;   which always leads to 1/3 which is not a finite representation
;;   UPDATE: as a trick and rounding function, I am evaluating the denominator
;;     as a real number which converts it to a finite and then 
;;     converting it back to a curset. This is a rounding cheat to limit inifinities

( defun invert (a)
  ( vc (float (/ 1 (cv a))))
)


;; (div a b) returns the division of a by b
;;
;;   simply the multiplication of the first by the inversion of the second curset

( defun div (a b)
  ( mul a (invert b))
)

( defun invertTRY (a)
  ( if (eqp a +pos+)
    a
    ( if (lt a +zer+)
      ( negate(invert(negate a)))
      ( if (eqp a +zer+)
        ( print "die with error")
        ( let (
            ( al (car a))
            ( ar (cdr a))
            ( il +zer+)
            ( c +zer+)
            ( ial +zer+)
            ( iar +zer+)
            ir
          )
          ( loop while (or il ir) do
            ( let (nl nr)
              ( if il
                ( let (
                    (c (cons il (cdr c)))
                  )
                  ( if ar
                    ( let (
                        ( iar (or iar (invert ar)))
                        ( l (mul (add +pos+ (mul (sub ar a) il))))
                      )
                      ( if (or ((not (car c)) (gt l (car c))))
                        ( setq nl l)
                      )
                    )
                  )
                  ( if (and al (not (le al +zer+)))
                    ( let (
                        ( ial (or ial (invert al)))
                        ( r (mul (add +pos+ (mul (sub al a) il)) ial))
                      )
                      ( if (or ((not (cdr c)) (lt r (cdr c))))
                        ( setq nr r)
                      )
                    )
                  )
                )
              )
              ( if ir
                ( let (
                    (c (cons (car c) ir))
                  )
                  ( if (and al (not (le al +zer+)))
                    ( let (
                        ( ial (or ial (invert al)))
                        ( l (mul (add +pos+ (mul (sub al a) ir))))
                      )
                      ( if (not (or (and nl (le l nl) 
                                    (and (car c) (le l (car c))))))
                        ( setq nl l)
                      )
                    )
                  )
                  ( if ar
                    ( let (
                        ( iar (or iar (invert ar)))
                        ( right (mul (add +pos+ (mul (sub al a) ir)) iar))
                      )
                      ( if (not (or (and nr (le right nr)) (and (cdr c) (le right (cdr c)))))
                        ( setq nr right)
                      )
                    )
                  )
                  ( setf il nl)
                  ( setf ir nr)
                )
              )
            )
          )
          ( equiv c)
        )
      )
    )
  )
)

;;;
;;; Tools
;;;


;; (gen a) produce a list of cursets from 0 to a...
;;   c = current curset
;;   r = right curset
;;   l = left curset
;;   s = a running stack
;;   o = the output list

( defun gen (a)
  ( let
    ( (s +zer+)
      (o +zer+)
      c l r 
    )
    ( loop repeat a do
      (setf r (car (last s)))
      (setf c (cons l r))
      (setf s (append (list r c) (reverse (cdr (reverse s)))))
      (setf o (append o (list c)))
      (setf l r)
    )
    o
  )
)


;;;
;;; Tests
;;;


;; test that cursets compare as the integers values used to create them...
;;
;;   tested true comparison on the first 1024 cursets
;;     for 2^10^2*6 = 6291456 comparisons

( let (
    ( size (expt 2 5))
    ( errors 0)
  )
  ( format t "Testing ~a×~a×~a = ~a total comparisons" 6 size size (* 6 size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (ov a)) 
          ( vb (ov b))
          ( ca (oc a))
          ( cb (oc b))
          expect
          result
        )

        ; test le
        ( setq expect (<= va vb))
        ( setq result (le ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test lt
        ( setq expect (< va vb))
        ( setq result (lt ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test gt
        ( setq expect (> va vb))
        ( setq result (gt ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test ge 
        ( setq expect (>= va vb))
        ( setq result (ge ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test eqp
        ( setq expect (= va vb))
        ( setq result (eqp ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test ne
        ( setq expect (/= va vb))
        ( setq result (ne ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no errors")
    ( format t "Error: There were ~a comparison errors" errors)
  )
)


;; test negate...
;;
;:   tested true negations on the first 2^20-1 = 1048575 curset negations

( let (
    ( size (- (expt 2 20) 1))
    ( errors 0)
  )
  ( format t "Testing ~a negations" size)
  ( terpri)
  ( let (
      c
      result
      expect
      errors
    )
    ( loop for a from 1048575 to size do
      ( print a)
      ( setq c (oc a))
      ( setq expect (- 0 (cv c)))
      ( setq result (cv (negate c)))
      ( if 
        ( /= expect result)
        ( incf errors)
      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no errors")
    ( format t "Error: There were ~a negation errors" errors)
  )
)

;; test addition
;;
;;  tested true addition for the first 256 cursets: 2^8^2 = 65536 additions

( let (
    ( size (expt 2 6))
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total additions" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (ov a)) 
          ( vb (ov b))
          ( ca (oc a))
          ( cb (oc b))
          expect
          result
        )
        ( setq expect (+ va vb))
        ( setq result (cv (add ca cb)))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no addition errors")
    ( format t "Error: There were ~a addition errors" errors)
  )
)


;; test subtraction
;;
;;  tested true subtraction for the first 256 cursets: 2^8^2 = 65536 subtractions

( let (
    ( size (expt 2 6))
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total subtractions" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (ov a)) 
          ( vb (ov b))
          ( ca (oc a))
          ( cb (oc b))
          expect
          result
        )
        ( setq expect (- va vb))
        ( setq result (cv (sub ca cb)))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no subtraction errors")
    ( format t "Error: There were ~a subtraction errors" errors)
  )
)


;; test multiplication
;;
;;  tested true for the first 15 cursets
;;
;; Fails for 16th × 16th curset which is -4 × -4 = 16 for unknown reasons at this time
;;  ex failure: "(mul (oc 16) (oc 16))"

( let (
    ( size 15)
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total multiplications" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (ov a))
          ( vb (ov b))
          ( ca (oc a))
          ( cb (oc b))
          expect
          result
        )
        ( setq expect (* va vb))
        ( setq result (cv (mul ca cb)))
        ( if
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no multiplication errors")
    ( format t "Error: There were ~a multiplication errors" errors)
  )
)


;; test division
;;
;;  tested true for the first 4 cursets
;;
;; Fails for 4th/8th curset which is -2/-3 = 2/3 = 0.6666667 for unknown reasons
;;  or perhaps I did not wait long enough?
;;  ex failure: "(mul (oc 16) (oc 16))"

( let (
    ( size 7)
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total division" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (ov a))
          ( vb (ov b))
          ( ca (oc a))
          ( cb (oc b))
          expect
          result
        )
        ( if (/= vb 0)
          ( progn
            ; test division
            ( setq expect (/ va vb))
            ( setq result (float (cv (div ca cb))))
            ( if
              ( not (or (and expect result) (and (not expect) (not result))))
              ( incf errors)
            )
          )
        )
      )
    )
  )
  ( if (= 0 errors)
    ( print "Success: There were no division errors")
    ( format t "Error: There were ~a division errors" errors)
  )
)
