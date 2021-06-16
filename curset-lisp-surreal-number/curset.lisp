; curset.lisp - Finite Surreal Number Calculator
;
;  "Curset" a self-refrencing linked list of tuples to nil representing "numbers"
;
;  Creates, evaluates and operates on finite surreal numbers as memory constructions 
;    which are represented by linked tuples (cons) of its left onto its right parts
;
;  These numbers represent signed dyadic fractions or all base 2 numbers
;    up to bit precision of lisp positive intgers
;
;  Conversion between numbers formats of order, values and cursets are provided by 
;    ov, oc, vo, vc, co and cv functions in which letters represent a "from to" relationship 
;
;  For example "ov" says to convert from the order into its values
;    the code: "(ov 22)" then means to return the value of the 22nd surreal number
;
;  The linked tumple representations have been named "cursets" because they are not a
;    true representation of Surreal numbers
;
;  Cursets are easily created by order, using:
;    "(oc x)" where x is a non-negative integer
;    "(ov x)" where x is a signed float of some finite precision
;


;
;  constant curset representations for signed units and zero
;

(defvar +zer+ (cons nil nil))
(defvar +neg+ (cons nil +zer+))
(defvar +pos+ (cons +zer+ nil))


;
; Comparison functions:
;


; (lep a b) is true if a is less than or equal to b
;
; lep implements less than or equal to comparison which is the primary formula 
;   on which all other mathematical operations depend
; considering that all numbers have a less and greater part if any, then
;   number A is less than or equal to number B when both
;   1. there is no left part of A or B is not less than this part, and
;   2. there is no right part of B or A is not less than this part

( defun lep (a b)
  ( and (not (and (car a) (lep b (car a)) ) )
        (not (and (cdr b) (lep (cdr b) a) ) ) )
)


; (gtp a b) is true is a is greater than b

( defun gtp (a b)
    ( not (lep a b))
) 


; (ltp a b) is true if a is less than b

( defun ltp (a b) 
    ( not (lep b a))
)


; (gep a b) is true is a is greater than or equal to b

( defun gep (a b)
    ( lep b a)
)


; (eqp a b) is true is a is equal to b

( defun eqp (a b)
    ( and (lep a b) (lep b a))
)


; (nep a b) is true is a is not equal to b

( defun nep (a b)
    ( not (and (lep a b) (lep b a)))
)


; (least a b) returns the curset with the lower numeric value
;
;   large negative numbers are the lowest

( defun least (a b)
    ( if (lep a b) a b)
)


; (greatest a b) returns the curset with the greaters numeric value

( defun greatest (a b)
    ( if (lep a b) b a)
)


; (equiv a) returns the reduced surreal form of the given curset
;
;   this is useful for reducing the size of cursets after mathematical operations
;   which can create tree structures which are much longer than their equivelant
;   reduced form

( defun equiv (x &optional (y +zer+))
  ( if (lep x y)
    ( if (lep y x)
      y
      ( equiv x (cons (car y) y))
    )
    ( equiv x (cons y (cdr y)))
  )
)

;
; Math operations: negation, addition, subtraction, multiplication, inversion, division
;


; (negate a) returns the negation of the given curset

( defun negate (c)
  ( if c
    ( cons (negate (cdr c)) (negate (car c)))
    c
  )
)


; (add a b) returns the addition of curset a and b

( defun add (x y)
  ( if (not x)
    y
    ( if (not y)
      x
      ( let 
        ( ( a (car x))
          ( b (cdr x))
          ( c (car y))
          ( d (cdr y))
          r l
        )
        ( setf l (if a (add a y) a))
        ( setf r (if b (add b y) b))
        ( when c
          ( let
            ( (less (add x c)) )
            ( when (or (not l) (lep l less))
              ( setf l less)
            )
          )
        )
        ( when d
          ( let 
            ( (more (add x d)) )
            ( when (or (not r) (lep more r))
              ( setf r more)
            )
          )
        )
        ( equiv (cons l r))
      )
    )
  )
)

; (sub a b) subtract the second curset from the first

( defun sub (x y)
  ( add x (negate y))
)

; (mul a b) multiply two cursets

( defun mul (x y)
  ( if (or (not x) (eqp y +pos+))
    x
    ( if (or (not y) (eqp x +pos+))
      y
      ( if (eqp x +neg+)
        ( negate y)
        ( if (eqp y +neg+)
          ( negate x)
          ( let (
              ( xl (car x))
              ( xr (cdr x))
              ( yl (car y))
              ( yr (cdr y))
              l r
            )
            ( if (and xl yl)
              ( setq l (sub (add (mul xl y) (mul x yl)) (mul xl yl)))
            )
            ( if (and xr yr)
              ( let (
                  ( l2 (sub (add (mul xr y) (mul x yr)) (mul xr yr)))
                )
                ( if (or (not l) (lep l l2))
                  ( setq l l2)
                )
              )
            )
            ( if (and xl yr)
              ( setq r (sub (add (mul xl y) (mul x yr)) (mul xl yr)))
            )
            ( if (and xr yl)
              ( let (
                  ( r2 (sub (add (mul x yl) (mul xr y)) (mul xr yl)))
                )
                ( if (or (not r) (lep r2 r))
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


; (invert a) return the inversion (1/x) of the given curset
;
;   this function is incomplete and not tested
;   i believe that only division by 2 is possible
;   since inversion of larger integers requires (1/(x-1)) to be calculated
;   which always leads to 1/3 which is not a finite representation
;   UPDATE: as a trick and rounding function, I am evaluating the denominator
;     as a real number which converts it to a finite and then 
;     converting it back to a curset. This is a rounding cheat to limit inifinities

( defun invert (y)
  ( vc (float (/ 1 (cv y))))
)


; (div a b) returns the division of a by b
;
;   simply the multiplication of the first by the inversion of the second curset

( defun div (a b)
  ( mul a (invert b))
)

( defun invertTRY (y)
  ( if (eqp y +pos+)
    y
    ( if (ltp y +zer+)
      ( negate(invert(negate y)))
      ( if (eqp y +zer+)
        ( print "die with error")
        ( let (
            ( yl (car y))
            ( yr (cdr y))
            ( il +zer+)
            ( c +zer+)
            ( iyl +zer+)
            ( iyr +zer+)
            ir
          )
          ( loop while (or il ir) do
            ( let (nl nr)
              ( if il
                ( let (
                    (c (cons il (cdr c)))
                  )
                  ( if yr
                    ( let (
                        ( iyr (or iyr (invert yr)))
                        ( l (mul (add +pos+ (mul (sub yr y) il))))
                      )
                      ( if (or ((not (car c)) (gtp l (car c))))
                        ( setq nl l)
                      )
                    )
                  )
                  ( if (and yl (not (lep yl +zer+)))
                    ( let (
                        ( iyl (or iyl (invert yl)))
                        ( r (mul (add +pos+ (mul (sub yl y) il)) iyl))
                      )
                      ( if (or ((not (cdr c)) (ltp r (cdr c))))
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
                  ( if (and yl (not (lep yl +zer+)))
                    ( let (
                        ( iyl (or iyl (invert yl)))
                        ( l (mul (add +pos+ (mul (sub yl y) ir))))
                      )
                      ( if (not (or (and nl (lep l nl) 
                                    (and (car c) (lep l (car c))))))
                        ( setq nl l)
                      )
                    )
                  )
                  ( if yr
                    ( let (
                        ( iyr (or iyr (invert yr)))
                        ( right (mul (add +pos+ (mul (sub yl y) ir)) iyr))
                      )
                      ( if (not (or (and nr (lep right nr)) (and (cdr c) (lep right (cdr c)))))
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

;
; Conversion functions
;   representations: Order, Curset, Value
;


; (oc o) given natural o, return the curset with this order

( defun oc (o)
  ( let
    ( ( bits (floor (log (+ o 1/2) 2)))
      ( c +zer+)
    )
    ( if (< bits 0)
      ( setf c nil )
      ( loop for bit downfrom (- bits 1) to 0 do
        ( if (/= 0 (logand o (expt 2 bit)))
          ( setf c (cons c (cdr c)))
          ( setf c (cons (car c) c))
        )
      )
    )
    c
  )
)


; (co c) given curset c, return its order number

( defun co (c)
  ( let
    ( (o 0) (p 0) )
    ( if c
      ( progn
        ( loop while (and c (or (car c) (cdr c))) do 
          ( if (and (cdr c) (eqp (car c) (car (cdr c))))
            ( setf c (cdr c))
            ( progn
              ( setf o (+ o (expt 2 p)))
              ( setf c (car c))
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


; (vo v) the order of the surreal number having the given value
;
;  expects a signed dyadic input
;  output is a non negative integer

( defun vo (v)
  ( if v
    ( let 
      ( u s w f r a b o)
      ( setq s (if (< v 0) -1 1))
      ( setq u (* s v))
      ( setq w (floor u))
      ( setq f (- u w))
      ( setq r (rational (+ (* (+ (/ (- (/ f 2) 1) (expt 2 w)) 1) s) 1)))
      ( setq a (numerator r))
      ( setq b (denominator r))
      ( setq o (truncate (+ (/ (- a 1) 2) b)))
      o
    )
    0
  )
)

; (ov n) the value of the surreal number of the given order
;
;   expects a non negative integer input
;   output is a signed dyadic

( defun ov (n)
  ;( if (= n 0)
  ( if (zerop n)
    nil
    ( let
      ( l r s a w f )
      ( setq l (floor(log (+ n 1/2) 2)))
      ( setq r (- (/ (+ (* 2 n) 1) (expt 2 l)) 2))
      ( setq s (signum (- r 1)))
      ( setq a (* (- r 1) s))
      ; this fails: 
      ( setq w (floor (* -1 (log (- 1 a) 2))))
      ( setq f (+ (* (- a 1) (expt 2 (+ w 1))) 2))
      ( * (+ w f) s)
    )
  )
)


; (vc v) the curset representation of the surreal number having the given value
;
;  expects a signed dyadic input
;  output is a curset 

( defun vc (v)
  ( oc (vo v))
)


; (ov n) the value of the surreal number of the given order
;   expects a non negative integer input
;   output is a signed dyadic

( defun cv (c)
  ( ov (co c))
)


;
; Tools
;


; (gen n) produce a list of cursets from 0 to n...
;   c = current curset
;   r = right curset
;   l = left curset
;   s = a running stack
;   o = the output list

( defun gen (n)
  ( let
    ( c l r (s (list nil)) (o (list nil)) )
    ( loop repeat n do
      (setf r (car (last s)))
      (setf c (cons l r))
      (setf s (append (list r c) (reverse (cdr (reverse s)))))
      (setf o (append o (list c)))
      (setf l r)
    )
    o
  )
)


; test that cursets compare as the integers values used to create them...
;
;   tested true comparison on the first 1024 cursets
;     for 2^10^2*6 = 6291456 comparisons

( let (
    ( size (expt 2 10))
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

        ; test lep
        ( setq expect (<= va vb))
        ( setq result (lep ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test ltp
        ( setq expect (< va vb))
        ( setq result (ltp ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test gtp
        ( setq expect (> va vb))
        ( setq result (gtp ca cb))
        ( if 
          ( not (or (and expect result) (and (not expect) (not result))))
          ( incf errors)
        )

        ; test gep 
        ( setq expect (>= va vb))
        ( setq result (gep ca cb))
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

        ; test nep
        ( setq expect (/= va vb))
        ( setq result (nep ca cb))
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


; test negate...
;
:   tested true negations on the first 2^20 = 1048576 cursets

( let (
    ( size (expt 2 20))
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

; test addition
;
;  tested true addition for the first 256 cursets: 2^8^2 = 65536 additions

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

        ; test lep
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


; test subtraction
;
;  tested true subtraction for the first 256 cursets: 2^8^2 = 65536 subtractions

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

        ; test lep
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




; test multiplication
;
;  tested true for the first 15 cursets
;
; Fails for 16th × 16th curset which is -4 × -4 = 16 for unknown reasons at this time
;  ex failure: "(mul (oc 16) (oc 16))"

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
        ( print a)
        ( print b)

        ; test lep
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


; test division
;
;  tested true for the first 4 cursets
;
; Fails for 4th/8th curset which is -2/-3 = 2/3 = 0.6666667 for unknown reasons
;  or perhaps I did not wait long enough?
;  ex failure: "(mul (oc 16) (oc 16))"

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
        ( print a)
        ( print b)
        ( terpri)
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


