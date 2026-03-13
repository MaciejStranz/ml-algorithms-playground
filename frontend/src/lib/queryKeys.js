export const queryKeys = {
    algorithms: ["algorithms"],
    datasets: ["datasets"],
    algorithmVariants: (task) => ["algorithmVariants", task ?? "all"],
    experiments: ["experiments"], 
};