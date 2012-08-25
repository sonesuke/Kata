module Kata where

-- |
--
-- >>> score [1]
-- Just 1
--
-- >>> score [1,2]
-- Just 3
-- 
-- >>> score [11]
-- Nothing
--
-- >>> score [3,8]
-- Nothing
--
-- >>> score [10, 3, 2, 1]
-- Just 21
--
-- >>> score [3, 7, 4, 3]
-- Just 21
--
-- >>> score (replicate 12 10)
-- Just 300

score' rolls = case rolls of
    rolls -> Just(sc 1 rolls)
    where 
          sc 10 rs = sum rs
          sc f rs = case rs of
            10:rs'  -> sc' 3 rs f rs'
            x:y:rs' | x + y == 10 -> sc' 3 rs f rs'
                    | otherwise   -> sc' 2 rs f rs'
            _       -> sum rs
            where
              sc' n r f rr = sum (take n r) + sc (f + 1) rr


validate_10_pin_over rolls
  | maximum rolls > 10 = Nothing
  | otherwise = Just rolls

validate_10_pin_over_2roll rolls = case rolls of
  rolls   | maximum (0:(map sum validate_frames)) > 10 -> Nothing
          | otherwise -> Just rolls
          where
            spl [] = []
            spl l = (take 2 l):(spl (drop 2 l)) 
            validate_frames = spl [x | x <- rolls, x /= 10]

-- score x =  validate_10_pin_over x >>= validate_10_pin_over_2roll >>= score'
score x = do
  rolls <- validate_10_pin_over x
  rolls <- validate_10_pin_over_2roll rolls
  score' rolls

