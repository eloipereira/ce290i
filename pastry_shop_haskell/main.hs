-- 1) Algebraic Data Types
-- 2) Pattern matching
-- 3) Type classes

-- data Item = Pastry String Int Float | Beverage String Int Float
--     deriving Show

-- name:: Item -> String
-- name (Pastry n _ _) = n 
-- name (Beverage n _ _) = n

import Data.Map hiding (map)

data Item = Pastry {name:: String, weight:: Int, cost:: Float} 
          | Beverage {name:: String, capacity:: Int, cost:: Float} 

instance Show Item where
    show (Pastry n w c) = n ++ " weighting " ++ show(w) ++ "g and costing $" ++ show(c) ++ " to bake."
    show (Beverage n cp c) = n ++ " with capacity " ++ show(cp) ++ "ml and costing $" ++ show(c) ++ " to brew."

add:: Item -> Item -> Item
(Beverage n0 cp0 c0) `add` (Beverage n1 cp1 c1) = (Beverage (n0++ "_with_" ++n1) (cp0+cp1) (c0+c1))

data PastryShop = PastryShop {items:: Map String [Item] ,funds:: Float, margin:: Float}

bake_or_brew:: Item -> PastryShop -> PastryShop
bake_or_brew i ps
    | cost i > funds ps = ps
    | notMember (name i) (items ps) = (PastryShop new_is new_funds (margin ps))
    | member (name i) (items ps) = (PastryShop adj_is new_funds (margin ps))
    where new_funds = funds ps - cost i
          new_is = insert (name i) ([i]) (items ps)
          adj_is = adjust ([i]++) (name i) (items ps)

sell:: String -> PastryShop -> PastryShop
sell n ps
    | notMember n (items ps) = ps
    | length ((items ps) ! n) == 0 = ps
    | otherwise = PastryShop new_is new_funds (margin ps)
    where i = head ((items ps) ! n) 
          new_is = adjust (tail) n (items ps)
          new_funds = (1 + margin ps)*(cost i) + funds ps

main :: IO ()
main = do 
    mapM_ print [p,c,m,c_w_m]
    mapM_ print $ map (funds) [myShop, myShop0, myShop1]
    where p = Pastry "Croissant" 100 1.0 
          c = Beverage "Coffee" 10 0.5 
          m = Beverage "Milk" 20 0.5 
          c_w_m = c `add` m
          myShop = PastryShop empty 100 0.2
          myShop0 = (bake_or_brew c) . (bake_or_brew p) $ myShop 
          myShop1 = (sell "Coffee") . (sell "Croissant") $ myShop0
    