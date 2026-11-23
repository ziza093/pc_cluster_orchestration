const dbName = process.env.MONGO_DB_NAME;

db.getSiblingDB("admin").createUser({
  user: "useradmin",
  pwd: process.env.MONGO_USERADMIN_PASSWORD,
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
});

const appDb = db.getSiblingDB(dbName);

appDb.createUser({
  user: "cluster_owner",
  pwd: process.env.MONGO_OWNER_PASSWORD,
  roles: [{ role: "dbOwner", db: dbName }]
});

appDb.createUser({
  user: "cluster_app",
  pwd: process.env.MONGO_APP_PASSWORD,
  roles: [{ role: "readWrite", db: dbName }]
});