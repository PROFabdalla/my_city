from modeltranslation.translator import TranslationOptions, translator

from public_apps.company.models import Company


class CompanyTrans(TranslationOptions):
    fields = ("title", "business_description")


translator.register(Company, CompanyTrans)
