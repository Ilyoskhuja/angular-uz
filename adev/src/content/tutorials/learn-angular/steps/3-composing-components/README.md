# Komponentlarni birlashtirish

Komponent shablonini, komponent logikasini va komponent stillarini yangilashni oʻrgandingiz, lekin komponentni ilovangizda qanday ishlatasiz?

Komponent konfiguratsiyasidagi `selector` xususiyati komponentga boshqa shablonda murojaat qilishda ishlatiladigan nom beradi. `selector`'dan HTML tegi kabi foydalanasiz, masalan, `app-user` shablonda `<app-user />` koʻrinishida boʻladi.

NOTE: [Asoslar qoʻllanmasida komponentlardan foydalanish](/essentials/components#using-components) haqida koʻproq bilib oling.

Bu mashgʻulotda komponentlarni qanday birlashtirishni oʻrganasiz.

<hr/>

Bu misolda ikkita komponent bor: `User` va `App`.

<docs-workflow>

<docs-step title="`User`'ga murojaat qoʻshing">
`App` shablonini `app-user` selektoridan foydalanadigan `User`'ga murojaat qoʻshib yangilang. `User`'ni `App`'ning imports massiviga qoʻshishni unutmang — bu uni `App` shablonida foydalanish uchun mavjud qiladi.

```angular-html
template: `<app-user />`, imports: [User]
```

Endi komponent `Username: youngTech` xabarini koʻrsatadi. Shablon kodini koʻproq markup qoʻshish uchun yangilashingiz mumkin.
</docs-step>

<docs-step title="Koʻproq markup qoʻshing">
Shablonda istalgan HTML markup'dan foydalanishingiz mumkin boʻlgani uchun, `App` shablonini yana koʻproq HTML elementlar qoʻshib yangilab koʻring. Bu misolda `<app-user>` elementining otasi sifatida `<section>` elementi qoʻshiladi.

```angular-html
template: `
<section><app-user /></section>
`,
```

</docs-step>

</docs-workflow>
Ilova gʻoyangizni amalga oshirish uchun kerak boʻlgancha HTML markup va komponentlardan foydalanishingiz mumkin. Hatto bitta sahifada komponentingizning bir nechta nusxasiga ega boʻlishingiz ham mumkin.

Bu ajoyib oʻtish boʻladi: komponentni maʼlumotlarga qarab shartli ravishda qanday koʻrsatish mumkin? Bilish uchun keyingi boʻlimga oʻting.
