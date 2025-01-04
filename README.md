# efento_temp Config

## 1. Install Git
```bash
sudo apt update
```
```bash
sudo apt install git
```

## 2. Install Wireguard

```bash
sudo apt install wireguard
```
```bash
sudo nano /etc/wireguard/wg0.conf
```
2.1 Paste config

## 3. Enable Wireguard
```bash
sudo systemctl enable wg-quick@wg0 
```

```bash
sudo systemctl start wg-quick@wg0 
```
```bash
sudo apt install resolvconf
```
```bash
sudo systemctl restart resolvconf
```
## 3. git clone

```bash
git clone https://github.com/MFsquare-maran/efento_temp.git
```

```bash
cd efento_temp/
```

## 3. install evento libary  & start

```bash
chmod +x setup_env.sh
```
```bash
./setup_env.sh
```

