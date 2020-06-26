db = db.getSiblingDB("MovieFlix");

db.users.createIndex({ email: 1 }, { unique: true });
