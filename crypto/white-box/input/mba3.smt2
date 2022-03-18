(let ((a!1 (bvmul #xfffffffffffffffb (bvnot (bvor (bvnot t) (bvnot u)))))
      (a!2 (bvmul #xfffffffffffffffb (bvnot (bvor t (bvnot u))))))
(let ((a!3 (bvadd a!1
                  (bvmul #x0000000000000005 u)
                  (bvor (bvnot t) u)
                  (bvmul #xffffffffffffffff (bvnot (bvor t u)))
                  a!2)))
(let ((a!4 (bvor (bvnot (bvor (bvnot x) (bvnot a!3))) (bvxor a!3 z)))
      (a!5 (bvmul #x0000000000000006 (bvnot (bvor x (bvnot a!3) z))))
      (a!6 (bvmul #x0000000000000002 (bvnot (bvor (bvnot x) a!3 z))))
      (a!7 (bvmul #x0000000000000006 (bvnot (bvor (bvnot x) (bvnot a!3) z))))
      (a!8 (bvmul #x0000000000000006 (bvnot (bvor x a!3 (bvnot z)))))
      (a!9 (bvmul #x0000000000000002 (bvnot (bvor x (bvnot a!3) (bvnot z)))))
      (a!10 (bvmul #x0000000000000006 (bvnot (bvor (bvnot x) a!3 (bvnot z)))))
      (a!11 (bvmul #x0000000000000006
                   (bvnot (bvor (bvnot x) (bvnot a!3) (bvnot z))))))
  (bvadd (bvmul #xfffffffffffffffe (bvnot a!4))
         (bvmul #xfffffffffffffffa (bvnot (bvxor x z)))
         (bvmul #x0000000000000008 (bvnot (bvor x a!3 z)))
         a!5
         a!6
         a!7
         a!8
         a!9
         a!10
         a!11))))
