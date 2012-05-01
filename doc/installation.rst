Installation
************

Buildout
========

Configuration du fichier *buildout.cfg*
---------------------------------------

* Section **[buildout]**, définir l'emplacement du paquet::

    find-links =
        ...
        http://pypi.auf.org/simple/auf.django.saml

* Section **[buildout]**, identifier le paquet à installer::
 
    eggs =
        ...
        auf.django.saml

* Section **[versions]**, choix de la version du paquet::

    auf.django.saml = x.x

Installation automatique via buildout
-------------------------------------

La configuration précédente va permettre à buildout de télécharger le paquet, 
l'installer et le rendre disponible pour le projet Django::

    bin/builout -c devel.cfg

Exemple minimaliste du fichier *buildout.cfg*
---------------------------------------------

::

    [buildout]
    versions = versions
    
    find-links = http://pypi.auf.org/simple/auf.recipe.django
        http://pypi.auf.org/simple/auf.django.saml
    
    eggs =
        auf.recipe.django
        auf.django.saml
    
    [versions]
    auf.django.saml = 1.0
    
    [django]  
    recipe = auf.recipe.django 
    wsgi=true  
    settings=production 
    extra-paths = project 
    eggs = ${buildout:eggs}

