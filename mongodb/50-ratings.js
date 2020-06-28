db = db.getSiblingDB("MovieFlix");

db.ratings.createIndex(
  {
    movie: 1,
    user: 1,
  },
  {
    unique: 1,
  }
);

db.ratings.insertOne({
  _id: BinData(3, "1rAVQm04S4OnpgNYljNOKQ=="),
  movie: BinData(3, "zXdk2j1LRcybql2/7NUYEg=="),
  user: "admin@movieflix.com",
  rating: 7.6,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "36KdQwmbRdS/Mt3LFMBzlw=="),
  movie: BinData(3, "2WVzJotuRYG+O07vWIkl7A=="),
  user: "admin@movieflix.com",
  rating: 7.4,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "VSMEdLguTW6kPOL+0+yG2w=="),
  movie: BinData(3, "HRhSS8clQsy6JUcL4M0wAw=="),
  user: "admin@movieflix.com",
  rating: 7.9,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "/lsrPNyMQ2KG8syfc6PAUQ=="),
  movie: BinData(3, "Hw3mcFWmQAeFIDB8FeC1Gw=="),
  user: "admin@movieflix.com",
  rating: 7.7,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "RvXM7ncDTJeIwyL3XSUg4Q=="),
  movie: BinData(3, "Q6DHE48TQjK4WdMU2joOJg=="),
  user: "admin@movieflix.com",
  rating: 7.5,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "0QIrjw9IRbu4o5fT2JIXpw=="),
  movie: BinData(3, "P5iyoXoyRhWAhgabsd9gyw=="),
  user: "admin@movieflix.com",
  rating: 7.6,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "hdde87XgRZCyoSL5GcJtnw=="),
  movie: BinData(3, "y41fXmNQSZC12m0QUgnrWQ=="),
  user: "admin@movieflix.com",
  rating: 7.7,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
db.ratings.insertOne({
  _id: BinData(3, "aOHf3cQiTLOvTlDkNLmytA=="),
  movie: BinData(3, "X/BbfU37QNKHjyFSc0tS/A=="),
  user: "admin@movieflix.com",
  rating: 8.1,
  created_at: ISODate("2020-06-27T08:35:30.287Z"),
  updated_at: ISODate("2020-06-27T08:35:30.287Z"),
});
