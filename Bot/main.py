from bot.telegram_bot import TelegramBot
import os

from ontology.recipes_ontology import RecipesOntology

token = os.getenv("TOKEN")
ontology_iri = os.getenv("ONTOLOGY_IRI")
bot = TelegramBot(token, RecipesOntology(ontology_iri))
bot.start()