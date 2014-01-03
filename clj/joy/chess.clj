;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
; @Setup Time:   Friday, 20 December 2013.
; @Updated Time: 2013-12-24 23:11:35
; @Description:  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(ns joy.chess)

(defn initial-board []
  [\r \n \b \q \k \b \n \r
   \p \p \p \p \p \p \p \p
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \- \- \- \- \- \- \- \-
   \P \P \P \P \P \P \P \P
   \R \N \B \Q \K \B \N \R])


(def *file-key* \a)
(def *rank-key* \0)

(defn- file-component [file]
  (- (int file) (int  *file-key*)))

(defn- rank-component [rank]
  (* 8 (- 8 (- (int rank) (int *rank-key*)))))

(defn- index [file rank]
  (+ (file-component file) (rank-component rank)))

(defn lookup [board pos]
  (let [[file rank] pos]
    (board (index file rank))))

(letfn [(index [file rank]
          (let [f (- (int file) (int \a))
                r (* 8 (- 8 (- (int rank) (int \0))))]
            (+ f r)))]
  (defn lookup [board pos]
    (let [[file rank] pos]
      (board (index file rank)))))


(defn pos [e coll]
  (let [cmp (if (map? coll)
              #(= (val %1) %2)
              #(= %1 %2))]
    (loop [s coll, idx 0]
      (when (seq s)
        (if (cmp (first s) e)
          (if (map? coll)
            (key (first s))
            idx)
          (recur (rest s) (inc idx)))))))

(defn index [coll]
  (cond
   (map? coll) (seq coll)
   (set? coll) (map vector coll coll)
   :else (map vector (iterate inc 0) coll)))

(defn pos [e coll]
  (for [[i v] (index coll) :when (= e v)] i))


(defn xconj [t v]
  (cond
   (nil? t)	({:val v, :L nil :R nil})
   (< (:val t))	({:val	(:val t)
                  :L	(xconj (:L t) v)
                  :R	(:R t)})
   :else	({:val	(:val t)
                  :L	(:L t)
                  :R	(xconj (:R t) v)})))

(defn xseq [t]
  (when t
    (concat (xseq (:L t)) [(:va t)] (xseq (:R t)))))


(defn steps [xs]
  (if (empty? xs)
    []
    [(first xs) (steps (rest xs))]))

(defn rec-step [[x & xs]]
  (if x
    [x (rec-step xs)]
    []))

(defn make-fib [a b] (cons a (lazy-seq (make-fib  b (+ a b)))))

(defmacro letdefs [ss vs]
  (mapv eval
        (map (comp list* vector) (repeat 'def) ss vs)))

(defmacro letdefs2 [ss vs]
  `(do
     ~@(map (comp list* vector) (repeat 'def) ss vs)))


(fn parse [expr]
  (fn [m]
    (for [e expr]
      (cond
       (contains? '#{a b} e) 	(m e)
       (symbol? e) 		(eval e)
       :else			(parse e)))))

(defn gcd [x y]
  (cond
   (> x y) (recur (- x y) y)
   (< x y) (recur x (- y x))
   :else   x))
