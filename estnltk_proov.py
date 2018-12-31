# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 00:21:38 2018

@author: kalle

Käsud installimiseks:
[python 3.5, CMD admini õigustes
pip install estnltk==1.6.0b0
python -m estnltk.ner train_default_model
python -m nltk.downloader punkt
"""

# https://estnltk.github.io/estnltk/1.1/tutorials/morf_analysis.html
#with f as open('sõnapilv2.txt',encoding='utf-8'):
#    txt=f.read()
from estnltk import analyze
from pprint import pprint

pprint(analyze('Tüünete öötööde allmaaraudteejaam'))

"""
Hiina keel:

		
estnltk.PACKAGE_PATH	C:\Program Files\Python35\lib\site-packages\estnltk
estnltk.PACKAGE_PATH.capitalize	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.casefold	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.center	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.count	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.encode	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.endswith	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.expandtabs	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.find	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.format	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.format_map	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.index	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isalnum	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isalpha	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isdecimal	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isdigit	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isidentifier	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.islower	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isnumeric	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isprintable	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isspace	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.istitle	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.isupper	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.join	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.ljust	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.lower	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.lstrip	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.maketrans	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.partition	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.replace	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rfind	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rindex	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rjust	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rpartition	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rsplit	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.rstrip	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.split	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.splitlines	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.startswith	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.strip	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.swapcase	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.title	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.translate	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.upper	<class 'builtin_function_or_method'>
estnltk.PACKAGE_PATH.zfill	<class 'builtin_function_or_method'>
estnltk.Text	<class 'estnltk.text.Text'>
estnltk.Text.analyse	<class 'function'>
estnltk.Text.attributes	<class 'property'>
estnltk.Text.diff	<class 'function'>
estnltk.Text.list_layers	<class 'function'>
estnltk.Text.list_registered_layers	<class 'function'>
estnltk.Text.tag_layer	<class 'function'>
estnltk.Text.text	<class 'property'>
estnltk.core	<module 'estnltk.core' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\core.py'>
estnltk.core.PACKAGE_PATH	<class 'str'>
estnltk.core.os	<class 'module'>
estnltk.layer	<module 'estnltk.layer' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\layer.py'>
estnltk.layer.Layer	<class 'type'>
estnltk.layer.List	<class 'typing.GenericMeta'>
estnltk.layer.Span	<class 'type'>
estnltk.layer.SpanList	<class 'abc.ABCMeta'>
estnltk.layer.Tuple	<class 'typing.TupleMeta'>
estnltk.layer.Union	<class 'typing.UnionMeta'>
estnltk.layer.bisect	<class 'module'>
estnltk.layer.pandas	<class 'module'>
estnltk.layer.whitelist_record	<class 'function'>
estnltk.layer_operations	<module 'estnltk.layer_operations' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\layer_operations\\__init__.py'>
estnltk.layer_operations.apply_simple_filter	<class 'function'>
estnltk.layer_operations.conflict_resolver	<class 'module'>
estnltk.layer_operations.conflicts	<class 'function'>
estnltk.layer_operations.count_by	<class 'function'>
estnltk.layer_operations.count_by_document	<class 'function'>
estnltk.layer_operations.dict_to_df	<class 'function'>
estnltk.layer_operations.diff_layer	<class 'function'>
estnltk.layer_operations.extract_section	<class 'function'>
estnltk.layer_operations.extract_sections	<class 'function'>
estnltk.layer_operations.group_by_spans	<class 'function'>
estnltk.layer_operations.layer_operations	<class 'module'>
estnltk.layer_operations.merge_layer	<class 'function'>
estnltk.layer_operations.new_layer_with_regex	<class 'function'>
estnltk.layer_operations.rebase	<class 'function'>
estnltk.layer_operations.resolve_conflicts	<class 'function'>
estnltk.layer_operations.split_by	<class 'function'>
estnltk.layer_operations.split_by_sentences	<class 'function'>
estnltk.layer_operations.splitting	<class 'module'>
estnltk.layer_operations.unique_texts	<class 'function'>
estnltk.resolve_layer_dag	<module 'estnltk.resolve_layer_dag' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\resolve_layer_dag.py'>
estnltk.resolve_layer_dag.CompoundTokenTagger	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.DEFAULT_RESOLVER	<class 'estnltk.resolve_layer_dag.Resolver'>
estnltk.resolve_layer_dag.List	<class 'typing.GenericMeta'>
estnltk.resolve_layer_dag.MorphExtendedTagger	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.ParagraphTokenizer	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.Resolver	<class 'type'>
estnltk.resolve_layer_dag.SentenceTokenizer	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.Taggers	<class 'type'>
estnltk.resolve_layer_dag.TokensTagger	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.VabamorfTagger	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.WordTagger	<class 'abc.ABCMeta'>
estnltk.resolve_layer_dag.make_resolver	<class 'function'>
estnltk.resolve_layer_dag.nx	<class 'module'>
estnltk.rewriting	<module 'estnltk.rewriting' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\rewriting\\__init__.py'>
estnltk.rewriting.FiniteFormRewriter	<class 'type'>
estnltk.rewriting.LetterCaseRewriter	<class 'type'>
estnltk.rewriting.MorphAnalyzedToken	<class 'type'>
estnltk.rewriting.MorphExtendedRewriter	<class 'type'>
estnltk.rewriting.MorphToSyntaxMorphRewriter	<class 'type'>
estnltk.rewriting.PronounTypeRewriter	<class 'type'>
estnltk.rewriting.PunctuationTypeRewriter	<class 'type'>
estnltk.rewriting.RemoveAdpositionAnalysesRewriter	<class 'type'>
estnltk.rewriting.RemoveDuplicateAnalysesRewriter	<class 'type'>
estnltk.rewriting.ReverseRewriter	<class 'type'>
estnltk.rewriting.SubcatRewriter	<class 'type'>
estnltk.rewriting.VabamorfCorrectionRewriter	<class 'type'>
estnltk.rewriting.VerbExtensionSuffixRewriter	<class 'type'>
estnltk.rewriting.helpers	<class 'module'>
estnltk.rewriting.postmorph	<class 'module'>
estnltk.rewriting.rewriting	<class 'module'>
estnltk.rewriting.syntax_preprocessing	<class 'module'>
estnltk.spans	<module 'estnltk.spans' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\spans.py'>
estnltk.spans.Any	<class 'typing.AnyMeta'>
estnltk.spans.Layer	<class 'type'>
estnltk.spans.List	<class 'typing.GenericMeta'>
estnltk.spans.MutableMapping	<class 'typing.GenericMeta'>
estnltk.spans.Span	<class 'type'>
estnltk.spans.SpanList	<class 'abc.ABCMeta'>
estnltk.spans.Tuple	<class 'typing.TupleMeta'>
estnltk.spans.Union	<class 'typing.UnionMeta'>
estnltk.spans.bisect	<class 'module'>
estnltk.spans.collections	<class 'module'>
estnltk.spans.itertools	<class 'module'>
estnltk.taggers	<module 'estnltk.taggers' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\taggers\\__init__.py'>
estnltk.taggers.CompoundTokenTagger	<class 'abc.ABCMeta'>
estnltk.taggers.DateTagger	<class 'abc.ABCMeta'>
estnltk.taggers.EventSequenceTagger	<class 'abc.ABCMeta'>
estnltk.taggers.FiniteFormTagger	<class 'abc.ABCMeta'>
estnltk.taggers.MorphExtendedTagger	<class 'abc.ABCMeta'>
estnltk.taggers.ParagraphTokenizer	<class 'abc.ABCMeta'>
estnltk.taggers.PronounTypeTagger	<class 'abc.ABCMeta'>
estnltk.taggers.RegexTagger	<class 'abc.ABCMeta'>
estnltk.taggers.SentenceTokenizer	<class 'abc.ABCMeta'>
estnltk.taggers.SubcatTagger	<class 'abc.ABCMeta'>
estnltk.taggers.Tagger	<class 'abc.ABCMeta'>
estnltk.taggers.TokensTagger	<class 'abc.ABCMeta'>
estnltk.taggers.VabamorfTagger	<class 'abc.ABCMeta'>
estnltk.taggers.VerbExtensionSuffixTagger	<class 'abc.ABCMeta'>
estnltk.taggers.WordTagger	<class 'abc.ABCMeta'>
estnltk.taggers.event_tagging	<class 'module'>
estnltk.taggers.morf	<class 'module'>
estnltk.taggers.morf_common	<class 'module'>
estnltk.taggers.postanalysis_tagger	<class 'module'>
estnltk.taggers.raw_text_tagging	<class 'module'>
estnltk.taggers.syntax_preprocessing	<class 'module'>
estnltk.taggers.tagger	<class 'module'>
estnltk.taggers.text_segmentation	<class 'module'>
estnltk.text	<module 'estnltk.text' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\text.py'>
estnltk.text.DEFAULT_RESOLVER	<class 'estnltk.resolve_layer_dag.Resolver'>
estnltk.text.Layer	<class 'type'>
estnltk.text.List	<class 'typing.GenericMeta'>
estnltk.text.MutableMapping	<class 'typing.GenericMeta'>
estnltk.text.Sequence	<class 'typing.GenericMeta'>
estnltk.text.Span	<class 'type'>
estnltk.text.SpanList	<class 'abc.ABCMeta'>
estnltk.text.Text	<class 'type'>
estnltk.text.Union	<class 'typing.UnionMeta'>
estnltk.text.bisect_left	<class 'builtin_function_or_method'>
estnltk.text.defaultdict	<class 'type'>
estnltk.text.keyword	<class 'module'>
estnltk.text.nx	<class 'module'>
estnltk.text.pandas	<class 'module'>
estnltk.vabamorf	<module 'estnltk.vabamorf' from 'C:\\Program Files\\Python35\\lib\\site-packages\\estnltk\\vabamorf\\__init__.py'>
estnltk.vabamorf.absolute_import	<class '__future__._Feature'>
estnltk.vabamorf.atexit	<class 'module'>
estnltk.vabamorf.morf	<class 'module'>
estnltk.vabamorf.print_function	<class '__future__._Feature'>
estnltk.vabamorf.terminate	<class 'function'>
estnltk.vabamorf.unicode_literals	<class '__future__._Feature'>
estnltk.vabamorf.vabamorf	<class 'module'>
estnltk.vabamorf.vm	<class 'module'>
"""
