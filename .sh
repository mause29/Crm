# backup.sh
#!/bin/bash
TIMESTAMP=$(date +"%F-%H-%M")
MONGO_DB="crmDB"
BACKUP_DIR="/backups/crm"

mkdir -p $BACKUP_DIR/$TIMESTAMP
mongodump --db $MONGO_DB --out $BACKUP_DIR/$TIMESTAMP
# Opcional: eliminar backups antiguos
find $BACKUP_DIR/* -mtime +30 -exec rm -rf {} \;
