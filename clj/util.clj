;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; @Autor:        Isaac.Zeng ~~~ gaofeng.zeng@togic.com
; @Setup Time:   Thursday, 19 December 2013.
; @Updated Time: 2013-12-19 02:37:50
; @Description:  
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(ns clj.util)


(defn gen-dir-tree [dir]
  (let [[p & chlds] (clojure.string/split dir #"/")
        [p chlds] (if (seq p) [p chlds] [(str "/" (first chlds)) (next chlds)])]
    (loop [dirs [p]
           chlds chlds]
      (if (and  chlds (seq (first chlds)))
        (recur (conj dirs (str (last dirs) \/ (first chlds)))
               (next chlds))
        dirs))))

(defn mkdir [dir & [recur]]
  {:pre [(or (nil? recur)
             (false? recur)
             (true? recur))]}
  (if recur
    (boolean
     (reduce #(and %1 %2)
             (map #(.mkdir (try
                             (java.io.File. %)
                             (catch Exception e)))
                  (gen-dir-tree dir))))
    (.mkdir (java.io.File. dir))))

