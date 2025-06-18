library(FuzzyLP)
# Ograniczenia
constraints <- matrix(c(
  2, 10, 4,
  8, 1, 4,
  4, 0, 2,
  1, 0, 0,
  0, 0, 1,
  9, 19, 9,
  1, 1, 3,
  1, 3, 3
), nrow = 8, byrow = TRUE)
directions <- c("<=", "<=", "<=", ">=", ">=", ">=", "<=", "<=")
aspiration <- c(100, 50, 50, 3, 5, 150, 30, 70)
tolerance  <- c(10, 5, 0, 0, 0, 20, 5, 10)
# Funkcja celu
objectives <- list(
  income    = list(vec = c(9, 19, 9), target = 150, tol = 20, max = TRUE),
  emissions = list(vec = c(1, 1, 3), target = 30,  tol = 5,  max = FALSE),
  cost      = list(vec = c(1, 3, 3), target = 70,  tol = 10, max = FALSE),
  s1 = list(vec = c(2, 10, 4), target = 100, tol = 10, max = FALSE),
  s2 = list(vec = c(8, 1, 4), target = 50, tol = 5, max = FALSE)
)
# Funkcja wykonująca obliczenia
solve_and_show <- function(name, obj) {
  cat("\n===== CEL:", toupper(name), "=====\n")
  res <- FCLP.fuzzyObjective(
    obj$vec, constraints, directions, aspiration, tolerance,
    z0 = obj$target, t0 = obj$tol, maximum = obj$max, verbose = FALSE
  )
  x <- res[, c("x1", "x2", "x3")]
  cat("Rozwiązanie: x =", round(x, 3), "\n")
  cat("Income   =", sum(c(9,19,9) * x), "\n")
  cat("Emissions=", sum(c(1,1,3) * x), "\n")
  cat("Cost     =", sum(c(1,3,3) * x), "\n")
}
# Obliczenia dla każdego celu
for (name in names(objectives)) {
  solve_and_show(name, objectives[[name]])
}
