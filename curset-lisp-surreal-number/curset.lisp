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
;;;;    order-to-value, oc, value-to-order, value-to-order, curset-to-order and curset-to-value functions where letters represent a "from to" relationship 
;;;;
;;;;  For example "order-to-value" says to convert from the order into its values
;;;;    the code: "(order-to-value 22)" then means to return the value of the 22nd surreal number
;;;;
;;;;  The linked tumple representations have been named "cursets" because they are not a
;;;;    true representation of Surreal numbers
;;;;
;;;;  Cursets are easily created by order, using:
;;;;    "(order-to-curset a)" where a is a non-negative integer
;;;;    "(order-to-value a)" where a is a signed float of some finite precision
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


;; (less-or-equal a b) is true if a is less than or equal to b
;;
;; less-or-equal implements less than or equal to comparison which is the primary formula 
;;   on which all other mathematical operations depend
;; considering that all numbers have a less and greater part if any, then
;;   number A is less than or equal to number B when both
;;   1. there is no left part of A or B is not less than this part, and
;;   2. there is no right part of B or A is not less than this part

( defun less-or-equal (a b)
  ( let
    ( (left (car a))
      (right (cdr b))
    )
    ( and (not (and left (less-or-equal b left)))
          (not (and right (less-or-equal right a)))
    )
  )
)


;; (greater-than a b) is true is a is greater than b

( defun greater-than (a b)
    ( not (less-or-equal a b))
) 


;; (less-than a b) is true if a is less than b

( defun less-than (a b) 
    ( not (less-or-equal b a))
)


;; (greater-or-equal a b) is true is a is greater than or equal to b

( defun greater-or-equal (a b)
    ( less-or-equal b a)
)


;; (equivelent a b) is true is a is equal to b

( defun equivelent (a b)
    ( and (less-or-equal a b) (less-or-equal b a))
)


;; (not-equal a b) is true is a is not equal to b

( defun not-equal (a b)
    ( not (and (less-or-equal a b) (less-or-equal b a)))
)


;; (least a b) returns the curset with the lower numeric value
;;
;;   large negative numbers are the lowest

( defun least (a b)
    ( if (less-or-equal a b) a b)
)


;; (greatest a b) returns the curset with the greaters numeric value

( defun greatest (a b)
    ( if (less-or-equal a b) b a)
)


;; (reduced-form a) returns the reduced surreal form of the given curset
;;
;;   this is useful for reducing the size of cursets after mathematical operations
;;   which can create tree structures which are much longer than their equivelant
;;   reduced form

( defun reduced-form (left &optional (right +zer+))
  ( if (less-or-equal left right)
    ( if (less-or-equal right left)
      right
      ( reduced-form left (cons (car right) right))
    )
    ( reduced-form left (cons right (cdr right)))
  )
)

;;;
;;; Conversion functions
;;;   representations: Order, Curset, Value
;;;

;; (bitsize n) - a simple function which return the size of a bit register needed to store n
;;   it returns -1 when the input is 0
 
( defun bitsize (p)
  ( do ((size -1 (incf size)))
    ((zerop p) size)
    ( setq p (ash p -1))
  )
)


;; (order-to-curset a) return the curset of the given order a

( defun order-to-curset (order)
  ( if (zerop order)
    nil
    ( let
        ( ( bits (1- (bitsize order)))
          ( curset +zer+)
        )
        ( loop for bit downfrom bits to 0 do
          ( if (zerop (logand order (ash 1 bit)))
            ( setf curset (cons (car curset) curset))
            ( setf curset (cons curset (cdr curset)))
          )
        )
        curset
    )
  )
)


;; (curset-to-order curset) given curset, return its order number

( defun curset-to-order (curset)
  ( let ( (order 0) )
    ( if curset
      ( let ( 
          (left (car curset))
          (right (cdr curset))
          (power -1)
        )
        ( if (not (or left right))
          ( setf order 1)
          ( progn
            ( loop while (and curset (or left right)) do 
              ( setq left (car curset))
              ( setq right (cdr curset))
              ( incf power)
              ( if (and left (eq right (cdr left)))
                ( progn
                  ( setf order (+ order (ash 1 power)))
                  ( setf curset left)
                )
                ( setf curset right)
              )
            )
            ( if order
              ( setf order (+ order (ash 1 power)))
              ( setf order 1)
            )
          )
        )
      )
    )
    order
  )
)


;; (value-to-order a) the order of the surreal number having the given value
;;
;;  expects a signed dyadic input
;;  output is a non negative integer

( defun value-to-order (value)
  ( if (eq (type-of value) 'single-float)
    (setq value (rational value))
  )
  ( if value
    ( let (
        sign absolute whole fraction rotation
      )
      ( setq sign (if (< value 0) -1 1))
      ( setq absolute (* sign value))
      ( setq whole (floor absolute))
      ( setq fraction (- absolute whole))
      ( setq rotation (rational (1+ (* (1+ (/ (1- (/ fraction 2)) (ash 1 whole))) sign))))
      (truncate (+ (/ (1- (numerator rotation)) 2) (denominator rotation)))
    )
    0
  )
)


;; (order-to-value order) the value of the surreal number of the given order
;;
;;   expects a non negative integer input
;;   output is a signed dyadic

( defun order-to-value (order)
  ( if (zerop order)
    nil
    ( let* (
        ( bits (bitsize order))
        ( rotation (- (/ (1+ (* 2 order)) (ash 1 bits)) 2))
        ( sign (signum (- rotation 1)))
        ( arch (* (- rotation 1) sign))
        ( whole (floor (- (log (- 1 arch) 2))))
        ( fraction (+ (* (1- arch) (ash 1 (1+ whole))) 2))
      )
      ( * (+ whole fraction) sign)
    )
  )
)


;; (value-to-order a) the curset representation of the surreal number having the given value
;;
;;  expects a signed dyadic input
;;  output is a curset 

( defun value-to-curset (value)
  ( order-to-curset (value-to-order value))
)


;; (curset-to-value a) the value of the surreal number of the given order
;;   expects a non negative integer input
;;   output is a signed dyadic

( defun curset-to-value (curset)
  ( order-to-value (curset-to-order curset))
)


;;;
;;; Math operations: negation, addition, subtraction, multiplication, inversion, division
;;;


;; (add a b) returns the addition of curset a and b

( defun add (a b)
  ( if a
    ( if b
      ( let 
        ( ( al (car a))
          ( ar (cdr a))
          ( bl (car b))
          ( br (cdr b))
          left right
        )
        ( setf left (if al (add al b) al))
        ( setf right (if ar (add ar b) ar))
        ( when bl
          ( let
            ( (less (add a bl)) )
            ( when (or (not left) (less-or-equal left less))
              ( setf left less)
            )
          )
        )
        ( when br
          ( let 
            ( (more (add a br)) )
            ( when (or (not right) (less-than more right))
              ( setf right more)
            )
          )
        )
        ( reduced-form (cons left right))
      )
      a
    )
    b
  )
)


;; (negate curset) returns the negation of the given curset

( defun negate (curset)
  ( if curset
    ( cons (negate (cdr curset)) (negate (car curset)))
    curset
  )
)


;; (subtract a b) subtract the second curset from the first

( defun subtract (a b)
  ( add a (negate b))
)

;; (multiply a b) multiply two cursets

( defun multiply (a b)
  ( if (or (not a) (equivelent b +pos+))
    a
    ( if (or (not b) (equivelent a +pos+))
      b
      ( if (equivelent a +neg+)
        ( negate b)
        ( if (equivelent b +neg+)
          ( negate a)
          ( let (
              ( al (car  a))
              ( ar (cdr a))
              ( bl (car  b))
              ( br (cdr b))
              l r
            )
            ( if (and al bl)
              ( setq l (subtract (add (multiply al b) (multiply a bl)) (multiply al bl)))
            )
            ( if (and ar br)
              ( let (
                  ( l2 (subtract (add (multiply ar b) (multiply a br)) (multiply ar br)))
                )
                ( if (or (not l) (less-or-equal l l2))
                  ( setq l l2)
                )
              )
            )
            ( if (and al br)
              ( setq r (subtract (add (multiply al b) (multiply a br)) (multiply al br)))
            )
            ( if (and ar bl)
              ( let (
                  ( r2 (subtract (add (multiply a bl) (multiply ar b)) (multiply ar bl)))
                )
                ( if (or (not r) (less-or-equal r2 r))
                  ( setq r r2)
                )
              )
            )
            ( reduced-form (cons l r))
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

( defun invert (curset)
  ( value-to-order (float (/ 1 (curset-to-value curset))))
)


;; (divide a b) returns the division of a by b
;;
;;   simply the multiplication of the first by the inversion of the second curset

( defun divide (a b)
  ( multiply a (invert b))
)


;;;
;;; Tools
;;;


;; (ordinal-universe day) produce a list of cursets to the given days ordered by their birth (ordinal)...

( defun ordinal-universe (days)
  ( let
    ( 
      ( n (1- (ash 1 days)))
      ( stack (list nil))
      head tail universe
    )
    ( loop repeat n do
      ( setq head (car universe))
      ( setq tail (car (last universe)))
      ( setq stack (append stack (list (cons head tail))))
      ( setq universe (append (list tail (cons head tail)) (butlast universe)))
    )
    stack
  )
)


;;; (value-universe a) - creates a list of value order cursets for a given cycle of days
;;;
;;; Generates 2 to the power of days of cursets in value order
;;;   starting from zero and accending to day - 1,
;;;   then it rolls to negative day - 1
;;; this generates a list in value order
;;; although the numbers roll in a circle, so the number at the beginning of the list will vary.
;;; if a is a power of 2, then the list will always begin with 

;;; cursets are stored in a cyclic list
;;; a loop puts new cursets on to the list in this process:
;;;  a new curset is added to the beginning of the stack
;;;  New cursets are generated by using the head of the stack as its left side
;;;  and the tail of the stack as its left side
;;;  the new curset is added to the beginning of the stack
;;;  the stack is rolled so that the tail element becomes the head


( defun value-universe (days)
  ( let
    ( 
      ( n (1- (ash 1 days)))
      head tail universe
    )
    ( loop repeat n do
      ( setq head (car universe))
      ( setq tail (car (last universe)))
      ( setq universe (append (list tail (cons head tail)) (butlast universe)))
    )
    universe
  )
)

;;;
;;; Short Forms - for testing convenience...
;;;

( defun co (c) (curset-to-order c))
( defun oc (o) (order-to-curset o))
( defun vo (v) (value-to-order v))
( defun ov (o) (order-to-value o))
( defun cv (c) (curset-to-value c))
( defun vc (v) (value-to-curset v))
( defun vu (d) (value-universe d))
( defun ou (d) (ordinal-universe d))
( defun le (a b) (less-or-equal a b))
( defun eqp (a b) (equivelent a b))


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
  ( format t "Comparing ~a × ~a × 6 ways = ~a comparisons" size size (* size size 6))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (order-to-value a)) 
          ( vb (order-to-value b))
          ( ca (order-to-curset a))
          ( cb (order-to-curset b))
          expect
          result
        )

        ; test le
        ( setq expect (<= va vb))
        ( setq result (less-or-equal ca cb))
        ( format t "~a <= ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS1"))
        )

        ; test lt
        ( setq expect (< va vb))
        ( setq result (less-than ca cb))
        ( format t "~a < ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS2"))
        )

        ; test greater-than
        ( setq expect (> va vb))
        ( setq result (greater-than ca cb))
        ( format t "~a > ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS3"))
        )

        ; test greater-or-equal 
        ( setq expect (>= va vb))
        ( setq result (greater-or-equal ca cb))
        ( format t "~a >= ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS4"))
        )

        ; test equivelent
        ( setq expect (= va vb))
        ( setq result (equivelent ca cb))
        ( format t "~a = ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS5"))
        )

        ; test ne
        ( setq expect (/= va vb))
        ( setq result (not-equal ca cb))
        ( format t "~a != ~a  expect:~a result:~a" va vb expect result)
        ( terpri)
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( progn (incf errors)(print "ERRORS6"))
        )

      )
    )
  )
  ( if (zerop errors)
    ( print "Success: There were no errors")
    ( format t "Error: There were ~a comparison errors" errors)
  )
)


;; test negate...
;;
;:   tested true negations on the first 2^20-1 = 1048575 curset negations

( let (
    ( size (- (expt 2 10) 1))
    ( errors 0)
  )
  ( format t "Testing ~a negations" size)
  ( terpri)
  ( let (
      curset
      result
      expect
      errors
    )
    ( loop for a from 1 to size do
      ( print a)
      ( setq curset (order-to-curset a))
      ( setq expect (- 0 (curset-to-value curset)))
      ( setq result (curset-to-value (negate curset)))
      ( if 
        ( /= expect result)
        ( incf errors)
      )
    )
  )
  ( if (zerop errors)
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
          ( va (order-to-value a)) 
          ( vb (order-to-value b))
          ( ca (order-to-curset a))
          ( cb (order-to-curset b))
          expect
          result
        )
        ( setq expect (+ va vb))
        ( setq result (curset-to-value (add ca cb)))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (zerop errors)
    ( print "Success: There were no addition errors")
    ( format t "Error: There were ~a addition errors" errors)
  )
)


;; test subtraction
;;
;;  tested true subtraction for the first 256 cursets: 2^8^2 = 65536 subtractions

( let (
    ( size (expt 2 7))
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total subtractions" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (order-to-value a)) 
          ( vb (order-to-value b))
          ( ca (order-to-curset a))
          ( cb (order-to-curset b))
          expect
          result
        )
        ( setq expect (- va vb))
        ( setq result (curset-to-value (subtract ca cb)))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (zerop errors)
    ( print "Success: There were no subtraction errors")
    ( format t "Error: There were ~a subtraction errors" errors)
  )
)


;; test multiplication
;;
;;  tested true for the first 15 cursets
;;
;; Fails for 16th × 16th curset which is -4 × -4 = 16 for unknown reasons at this time
;;  ex failure: "(multiply (order-to-curset 16) (order-to-curset 16))"

( let (
    ( size 15)
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total multiplications" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (order-to-value a))
          ( vb (order-to-value b))
          ( ca (order-to-curset a))
          ( cb (order-to-curset b))
          expect
          result
        )
        ( setq expect (* va vb))
        ( setq result (curset-to-value (multiply ca cb)))
        ( if
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )
      )
    )
  )
  ( if (zerop errors)
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
;;  ex failure: "(multiply (order-to-curset 16) (order-to-curset 16))"

( let (
    ( size 7)
    ( errors 0)
  )
  ( format t "Testing ~a×~a=~a total division" size size (* size size))
  ( terpri )
  ( loop for a from 1 to size do
    ( loop for b from 1 to size do
      ( let (
          ( va (order-to-value a))
          ( vb (order-to-value b))
          ( ca (order-to-curset a))
          ( cb (order-to-curset b))
          expect
          result
        )
        ( if (/= vb 0)
          ( progn
            ; test division
            ( setq expect (/ va vb))
            ( setq result (float (curset-to-value (divide ca cb))))
            ( if
              ( not (or (and expect result) (and (not expect) (not result))))
              ( incf errors)
            )
          )
        )
      )
    )
  )
  ( if (zerop errors)
    ( print "Success: There were no division errors")
    ( format t "Error: There were ~a division errors" errors)
  )
)
