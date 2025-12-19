const fs = require('fs');

function scheduleRevenueUpload(csvPath) {
  if (!fs.existsSync(csvPath)) {
    console.error('CSV file not found:', csvPath);
    return;
  }

  console.log('Ready to upload revenue conversions from:', csvPath);
}

if (require.main === module) {
  scheduleRevenueUpload('../../data-templates/sample-conversion-upload.csv');
}
