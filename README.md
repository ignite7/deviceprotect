# Deviceprotect 🗂

Device protect is a **CLI** tool made in python to make it easy to encrypt 
or decrypt your files without remember the any password. **Warning** this 
is for encrypt or decrypt not large amounts of files, if you want to do it,
do it at your own risk.

## Setup 🧲

```bash
git clone https://github.com/ignite7/deviceprotect.git

cd deviceprotect/

pip install .
```

## Usage 📕

**Note** that when you use encrypt is **important to save in a safe place
the output** which contains an `summary.txt` with the logs and `backup.db`
which is used to decrypt files easily.

- Encrypt:

```bash
# One file
deviceprotect encrypt -f my_file.txt

# One directory
deviceprotect encrypt -d my_dir/

# Several files
deviceprotect encrypt -f my_file_1.txt -f my_file_2.txt

# Several directories
deviceprotect encrypt -d my_dir_1/ -d my_dir_2/

# Use multiple keys for several files
deviceprotect encrypt -f my_file_1.txt -f my_file_2.txt -m

# Use multiple keys for several directories
deviceprotect encrypt -d my_dir_1/ -d my_dir_2/ -m

# Save the output in a custom path
deviceprotect encrypt -f my_file.txt -s /tmp/new_path
```

- Decrypt:

```bash
# Boring way to decrypt files
deviceprotect -f my_file_1.txt -k this_is_my_key

# Boring way to decrypt directories
deviceprotect -d my_dir/ -k this_is_my_key

# Best way to decrypt files or directories
deviceprotect -b deviceprotect/backup.db
```

## Testing 🛠

Run the tests on your local machine with docker.

```bash
cd deviceprotect/

docker-compose up -d

docker exec -it container_name sh

python test/test.py
```

## Todo 📣

- Add more ways to save the output
- Lock database

## Thanks 👏

> **_Made with 💙 by:_** [Sergio van Berkel Acosta](https://www.sergiovanberkel.com/)
