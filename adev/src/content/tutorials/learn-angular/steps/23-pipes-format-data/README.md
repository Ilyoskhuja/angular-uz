# Pipe'lar bilan maʼlumotlarni formatlash

Pipe'larni sozlash orqali ulardan foydalanishni yanada kengaytirishingiz mumkin. Pipe'larni ularga parametrlar (options) uzatish orqali sozlash mumkin.

NOTE: [Chuqur qoʻllanmada pipe'lar bilan maʼlumotlarni formatlash](/guide/templates/pipes) haqida koʻproq bilib oling.

Bu mashgʻulotda bir nechta pipe'lar va pipe parametrlari bilan ishlaysiz.

<hr>

Pipe'ga parametr uzatish uchun `:` sintaksisidan va undan keyin parametr qiymatidan foydalaning. Mana bir misol:

```angular-html
template: `{{ date | date: 'medium' }}`;
```

Chiqish: `Jun 15, 2015, 9:43:11 PM`.

Endi pipe chiqishini sozlash vaqti:

<docs-workflow>

<docs-step title="`DecimalPipe` bilan sonni formatlang">

`app.ts` faylida shablonni `decimal` pipe'i uchun parametr qoʻshish orqali yangilang.

```angular-html {highlight:[2]}
template: ` ...
<li>Number with "decimal" {{ num | number: '3.2-2' }}</li>
`
```

NOTE: Bu qanday format? `DecimalPipe` parametri `digitsInfo` deb ataladi va u quyidagi formatdan foydalanadi: `{minIntegerDigits}.{minFractionDigits}-{maxFractionDigits}`

</docs-step>

<docs-step title="`DatePipe` bilan sanani formatlang">

Endi shablonni `date` pipe'idan foydalanish uchun yangilang.

```angular-html {highlight:[2]}
template: ` ...
<li>Date with "date" {{ birthday | date: 'medium' }}</li>
`
```

Qiziqarli boʻlishi uchun `date` uchun turli parametrlarni sinab koʻring. Koʻproq maʼlumotni [Angular hujjatlarida](guide/templates/pipes) topishingiz mumkin.

</docs-step>

<docs-step title="`CurrencyPipe` bilan valyutani formatlang">

Oxirgi vazifangiz uchun shablonni `currency` pipe'idan foydalanish uchun yangilang.

```angular-html {highlight:[2]}
template: ` ...
<li>Currency with "currency" {{ cost | currency }}</li>
`
```

`currency` uchun ham turli parametrlarni sinab koʻrishingiz mumkin. Koʻproq maʼlumotni [Angular hujjatlarida](guide/templates/pipes) topishingiz mumkin.

</docs-step>

</docs-workflow>

Pipe'lar bilan ajoyib ish. Hozirgacha katta yutuqlarga erishdingiz.

Ilovalaringizda ishlatishingiz mumkin boʻlgan yana koʻplab oʻrnatilgan pipe'lar mavjud. Roʻyxatni [Angular hujjatlarida](guide/templates/pipes) topishingiz mumkin.

Oʻrnatilgan pipe'lar ehtiyojlaringizni qoplamasa, maxsus pipe ham yaratishingiz mumkin. Koʻproq bilish uchun keyingi darsga qarang.
