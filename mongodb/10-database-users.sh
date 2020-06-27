set -e

mongo <<EOF
db = db.getSiblingDB('admin');

db.createUser({
  user: '${MONGODB_USERNAME:-movieflix}',
  pwd: '${MONGODB_PASSWORD:-movieflix}',
  roles: [{
    role: 'readWrite',
    db: '${MONGODB_DB:-MovieFlix}',
  }],
});
EOF
