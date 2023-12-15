# Documentation technique

## **Documentation Technique: Collecte de Logs**

La présente section détaille les procédures et configurations associées à la récolte des logs dans l'application. Les mécanismes de collecte, les formats des logs, les options de configuration, ainsi que des instructions détaillées pour l'intégration dans divers environnements sont présentés ci-dessous.

### Mécanismes de Collecte des Logs

#### Points d'Intégration

L'application mise sur un mécanisme de collecte des logs basé sur une connexion SSH, permettant d'extraire les logs depuis une station distante. La flexibilité de la collecte des logs est assurée par la configuration ajustable pour s'adapter aux besoins spécifiques de l'environnement.

#### Configuration de la Collecte

La collecte des logs est configurée en adaptant les paramètres dans le script Python dédié. Les variables telles que les informations d'identification, le chemin distant des logs, et l'intervalle de collecte peuvent être personnalisées pour répondre aux exigences spécifiques.

### Formats et Contenu des Logs

#### Format des Fichiers CSV

Les logs sont stockés dans des fichiers CSV, où une nouvelle ligne est ajoutée à chaque minute. Chaque ligne contient le timestamp actuel et les logs récupérés depuis la station distante.

#### Contenu Typique des Logs

Le contenu des logs peut inclure diverses informations telles que les événements système, les erreurs, les avertissements, etc. La nature spécifique des logs dépend du système distant et des applications en cours d'exécution.

### Options de Configuration

#### Personnalisation des Paramètres

1. **Hostname**: L'adresse de la station distante.
2. **Username/Password**: Les informations d'identification pour la connexion SSH.
3. **Remote Log Path**: Le chemin distant vers les fichiers de logs.
4. **Interval**: L'intervalle entre chaque collecte de logs.

#### Exemples de Configurations

```python
hostname = 'remote_host'
username = 'user'
password = 'pass'
remote_log_path = '/path/to/remote/logs'
```

### Instructions Pas à Pas pour l'Intégration

#### Prérequis

- Assurez-vous que Python est installé sur le système local.
- Installez la bibliothèque Paramiko à l'aide de `pip install paramiko`.

#### Étapes d'Intégration

1. **Téléchargez le script de collecte des logs depuis le référentiel de l'application.**
2. **Configurez les paramètres dans le script en fonction de votre environnement.**
3. **Exécutez le script en utilisant la commande `python log_collection_script.py`.**
4. **Vérifiez les fichiers CSV générés pour les logs récupérés.**

---

## **Documentation Technique: Collecte de Métriques**

La section suivante détaille la collecte de métriques dans l'application, couvrant les mécanismes de collecte, les formats des métriques, les options de configuration et les instructions pas à pas pour l'intégration dans divers environnements.

### Mécanismes de Collecte de Métriques

#### Points d'Intégration

L'application utilise un script dédié pour collecter les métriques de performance, telles que l'utilisation du CPU, de la mémoire et du disque. La collecte peut être configurée pour s'adapter aux besoins spécifiques de l'environnement.

#### Configuration de la Collecte

La collecte des métriques est configurée en ajustant les seuils d'alerte dans le script Python dédié. Les variables telles que les seuils CPU, mémoire et disque peuvent être personnalisées pour répondre aux exigences spécifiques.

### Formats et Contenu des Métriques

#### Format des Fichiers CSV

Les métriques sont enregistrées dans des fichiers CSV, avec un timestamp associé à chaque collecte. Chaque ligne contient les valeurs des métriques collectées, permettant une analyse facile des performances.

#### Contenu Typique des Métriques

Le contenu des métriques peut inclure l'utilisation du CPU, de la mémoire, du disque, etc. Les valeurs spécifiques dépendent du système sur lequel l'application est déployée.

### Options de Configuration

#### Personnalisation des Seuils d'Alerte

1. **CPU Threshold**: Pourcentage d'utilisation du CPU déclenchant une alerte.
2. **Memory Threshold**: Pourcentage d'utilisation de la mémoire déclenchant une alerte.
3. **Disk Threshold**: Pourcentage d'utilisation du disque déclenchant une alerte.

#### Exemples de Configurations

```python
cpu_threshold = 80  # Pourcentage d'utilisation du CPU
memory_threshold = 80  # Pourcentage d'utilisation de la mémoire
disk_threshold = 80  # Pourcentage d'utilisation du disque
```

### Instructions Pas à Pas pour l'Intégration

#### Prérequis

- Assurez-vous que Python est installé sur le système local.
- Installez la bibliothèque psutil à l'aide de `pip install psutil`.

#### Étapes d'Intégration

1. **Téléchargez le script de collecte des métriques depuis le référentiel de l'application.**
2. **Configurez les seuils d'alerte dans le script en fonction de vos exigences.**
3. **Exécutez le script en utilisant la commande `python metric_collection_script.py`.**
4. **Surveillez la console pour les alertes en cas de dépassement des seuils définis.**