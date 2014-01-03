;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
; @Setup Time:   Tuesday, 24 December 2013.
; @Updated Time: 2013-12-25 02:10:07
; @Description:  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(ns joy.cps)

(defn fac-cps [n k]
  (letfn [(cont [v] (k (* v n)))]
    (if (zero? n)
      (k 1)
      (recur (dec n) cont))))
(defn fac [n]
  (fac-cps n identity))

(defn mk-cps [accept? end-value kend kont]
  (fn [n]
    ((fn [n k]
       (let [cont (fn [v] (k (kont v n)))]
         (if (accept? n)
           (k end-value)
           (recur (dec n) cont))))
     n kend)))

(defn ^long coeff [^long n]
  (if (even? n) 1 -1))


(def pi-value (mk-cps zero? 0 identity
                      (fn [v n]
                        (+ v (* (coeff n) (/ 1.0 (+ (* 2 n) 1)))))))

(defn ^double pi-value [^long n]
  ((fn ^double pi-value-iter [^long n ^double acc]
     (if (zero? n)
       acc
       (recur (dec n) (+ acc
                         (* (coeff n)
                            (/ 1.0
                               (+ (* 2 n) 1)))))))
   n 1))

(defn fib [n]
  (if (< n 2)
    n
    (+ (fib (dec n)) (fib (- n 2)))))

(defn ^long hint-fib [^long n]
  (if (< n 2)
    n
    (+ (fib (dec n)) (fib (- n 2)))))

(defn contextual-eval [expr ctx]
  (eval
   `(let [~@(mapcat (fn [[k v]] [k `'~v]) ctx)]
      ~expr)))

((fn [expr ctx]
   (eval
    `(let [~@(mapcat (fn [[k v]] [k `'~v]) ctx)]
       ~expr))))

(def ctx-eval
  (fn [expr]
    (fn [ctx]
      (eval
       `(let [~@(mapcat (fn [[k v]] [k `'~v]) ctx)]
          ~expr)))))

(= 2 (( '(/ a b))
      '{b 8 a 16}))

(defn ctx-eval [expr]
  (fn [ctx]
    (let [{a 'a b 'b} ctx]
      `(eval ~expr))))
