function calculateCostPerLead(cost, leads) {
  if (leads === 0) {
    return 0;
  }
  return cost / leads;
}

if (require.main === module) {
  const cost = 3000;
  const leads = 15;
  console.log('Cost per lead:', calculateCostPerLead(cost, leads));
}
