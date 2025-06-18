# Sets
set PLANTS;       # Plants (W1, W2)
set PRODUCTS;     # Products (P1, P2)
set WAREHOUSES;   # Warehouses (M1, M2, M3)
set STORES;       # Retail stores (S1, S2, S3, S4)
set SIZES {WAREHOUSES}; # Possible sizes for each warehouse

# Parameters
param max_production {PLANTS, PRODUCTS} >= 0;
param warehouse_capacity {w in WAREHOUSES, s in SIZES[w]} >= 0;
param warehouse_cost {w in WAREHOUSES, s in SIZES[w]} >= 0;
param module_capacity > 0;
param module_cost > 0;
param demand {PRODUCTS, STORES} >= 0;
param plant_to_warehouse_cost {PLANTS, WAREHOUSES} >= 0;
param warehouse_to_store_cost {WAREHOUSES, STORES} >= 0;

# Variables
var x {p in PLANTS, w in WAREHOUSES, r in PRODUCTS} >= 0;
var y {w in WAREHOUSES, s in STORES, r in PRODUCTS} >= 0;
var z {w in WAREHOUSES, s in SIZES[w]} binary;
var modules >= 0, integer;

# Objective function: Minimize total daily cost
minimize TotalCost:
    # Transportation costs from plants to warehouses
    sum {p in PLANTS, w in WAREHOUSES, r in PRODUCTS} 
        plant_to_warehouse_cost[p,w] * x[p,w,r] +
    # Transportation costs from warehouses to stores
    sum {w in WAREHOUSES, s in STORES, r in PRODUCTS} 
        warehouse_to_store_cost[w,s] * y[w,s,r] +
    # Warehouse operational costs for M1 and M2
    sum {w in WAREHOUSES, s in SIZES[w]: w != "M3"} 
        warehouse_cost[w,s] * z[w,s] +
    module_cost * modules;

# Constraints
subject to ProductionCapacity {p in PLANTS, r in PRODUCTS}:
    sum {w in WAREHOUSES} x[p,w,r] <= max_production[p,r];

subject to DemandSatisfaction {s in STORES, r in PRODUCTS}:
    sum {w in WAREHOUSES} y[w,s,r] = demand[r,s];

subject to FlowConservation {w in WAREHOUSES, r in PRODUCTS}:
    sum {p in PLANTS} x[p,w,r] = sum {s in STORES} y[w,s,r];

subject to WarehouseCapacity {w in WAREHOUSES: w != "M3"}:
    sum {p in PLANTS, r in PRODUCTS} x[p,w,r] <= 
    sum {s in SIZES[w]} warehouse_capacity[w,s] * z[w,s];

subject to WarehouseCapacityM3:
    sum {p in PLANTS, r in PRODUCTS} x[p,"M3",r] <= module_capacity * modules;

subject to OneSizePerWarehouse {w in WAREHOUSES: w != "M3"}:
    sum {s in SIZES[w]} z[w,s] = 1;
    
    
    