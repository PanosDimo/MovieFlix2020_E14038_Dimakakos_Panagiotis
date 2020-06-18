set -e

mongo <<EOF
movieflix = db.getSiblingDB('${MONGODB_DB:-MovieFlix}');

// Create admin user.
movieflix.users.insert({
  _id: BinData(3, 'KJ8cKJ3BS8+vSrnph5T4dQ=='),
  name: 'admin',
  email: 'admin@movieflix.com',
  password: BinData(0, 'JDJiJDEwJFhoZGJpbHpxT0ozV045WWk5LkNSQS5wNlAuR0FLWHpHanQvMUQyM3dNRkpnRXIzdENYRG1l'),
  comments: [],
  category: 'ADMIN',
});
EOF
