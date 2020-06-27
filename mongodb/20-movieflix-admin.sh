set -e

mongo <<EOF
movieflix = db.getSiblingDB('${MONGODB_DB:-MovieFlix}');

// Create admin user.
movieflix.users.insertOne({
  _id: BinData(3, 'KJ8cKJ3BS8+vSrnph5T4dQ=='),
  name: 'admin',
  email: 'admin@movieflix.com',
  password: BinData(0, 'JDJiJDEwJFhoZGJpbHpxT0ozV045WWk5LkNSQS5wNlAuR0FLWHpHanQvMUQyM3dNRkpnRXIzdENYRG1l'),
  comments: [BinData(3, 'gYpLiW0KRAmRQ7Y3AJeA0w==')],
  category: 'ADMIN',
  created_at: ISODate('2020-06-27T08:35:30.287Z'),
  updated_at: ISODate('2020-06-27T08:35:30.287Z'),
});
EOF
