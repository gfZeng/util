(defmacro spy-env []
  (let [ks (keys &env)]
    `(prn (zipmap '~ks [~@ks]))))

(defmacro spy-env- []
  (let [ks (keys &env)]
    (prn ks)
    (prn (zipmap ks (map eval `[~@ks])))))

;;; 
(defn spy-env-fn []
  (let [ks (keys &env)]
    (prn (zipmap ks (map eval ks)))))
