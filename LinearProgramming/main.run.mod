model main.mod;
data main.dat;

option solver gurobi;
solve;

display TotalCost;

display z;
display modules;

display x;
display y;

printf "Ca³kowity koszt magazynowania: %g\n", 
    (sum {w in WAREHOUSES, s in SIZES[w]: w != "M3"} warehouse_cost[w,s] * z[w,s]) + 
    (module_cost * modules);

printf "Ca³kowity koszt transportu: %g\n", 
    (sum {p in PLANTS, w in WAREHOUSES, r in PRODUCTS} plant_to_warehouse_cost[p,w] * x[p,w,r]) + 
    (sum {w in WAREHOUSES, s in STORES, r in PRODUCTS} warehouse_to_store_cost[w,s] * y[w,s,r]);

printf "\nU¿ycie magazynu:\n";
for {w in WAREHOUSES} {
    printf "Magazyn %s: ", w;
    if w == "M3" then {
        printf "%g jednostek (pojemnoœæ: %g)\n", 
            sum {p in PLANTS, r in PRODUCTS} x[p,w,r],
            module_capacity * modules;
    } else {
        printf "%g jednostek (pojemnoœæ: %g)\n", 
            sum {p in PLANTS, r in PRODUCTS} x[p,w,r],
            sum {s in SIZES[w]} warehouse_capacity[w,s] * z[w,s];
    }
}

