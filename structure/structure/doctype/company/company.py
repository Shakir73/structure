# -*- coding: utf-8 -*-
# Copyright (c) 2020, AFS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, os, json
from frappe import _
from frappe.utils import get_timestamp

from frappe.utils import cint, today, formatdate
import frappe.defaults
from frappe.cache_manager import clear_defaults_cache

from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.utils.nestedset import NestedSet

from past.builtins import cmp
import functools

class Company(NestedSet):
	nsm_parent_field = 'parent_company'

	def validate(self):
		self.validate_abbr()
		self.validate_currency()
		self.check_country_change()
		self.validate_parent_company()

	def validate_abbr(self):
		if not self.abbr:
			self.abbr = ''.join([c[0] for c in self.company.name.split()]).upper()

		self.abbr = self.abbr.strip()

		if not self.abbr.strip():
			frappe.throw(_("Abbreviation is mandatory"))

		if frappe.db.sql("select abbr from tabCompany where name!=%s and abbr=%s", (self.name, self.abbr)):
			frappe.throw(_("Abbreviation already used for another company"))

	def validate_currency(self):
		if self.is_new():
			return
		self.previous_default_currency = frappe.get_cached_value('Company',  self.name,  "default_currency")
		if self.default_currency and self.previous_default_currency and \
			self.default_currency != self.previous_default_currency and \
			self.check_if_transactions_exist():
				frappe.throw(_("Cannot change company's default currency, because there are existing transactions. Transactions must be cancelled to change the default currency."))

	def check_country_change(self):
		frappe.flags.country_change = False

		if not self.get('__islocal') and \
			self.country != frappe.get_cached_value('Company',  self.name,  'country'):
			frappe.flags.country_change = True

	def abbreviate(self):
		self.abbr = ''.join([c[0].upper() for c in self.company_name.split()])

	def validate_parent_company(self):
		if self.parent_company:
			is_group = frappe.get_value('Company', self.parent_company, 'is_group')

			if not is_group:
				frappe.throw(_('Parent Company must be a group company'))

def get_name_with_abbr(name, company):
	company_abbr = frappe.get_cached_value('Company', company, 'abbr')
	parts = name.split(" - ")

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)

	