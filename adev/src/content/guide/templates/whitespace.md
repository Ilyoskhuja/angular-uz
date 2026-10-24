# Shablonlardagi boʻshliqlar

Sukut boʻyicha Angular shablonlari freymvork keraksiz deb hisoblagan boʻshliqlarni (whitespace) saqlamaydi. Bu odatda ikki holatda yuz beradi: elementlar orasidagi boʻshliqlar va matn ichidagi qisqartiriladigan boʻshliqlar.

## Elementlar orasidagi boʻshliqlar {#whitespace-between-elements}

Koʻpchilik dasturchilar shablon oʻqilishi oson boʻlishi uchun uni yangi qatorlar va chekinishlar (indentation) bilan formatlashni afzal koʻradi:

```html
<section>
  <h3>User profile</h3>
  <label>
    User name
    <input />
  </label>
</section>
```

Bu shablon barcha elementlar orasida boʻshliqlarni oʻz ichiga oladi. Quyidagi fragment xuddi shu HTML'ni koʻrsatadi, lekin boʻshliqning qanchalik koʻp ekanini taʼkidlash uchun har bir boʻshliq belgisi panjara (`#`) belgisi bilan almashtirilgan:

<!-- prettier-ignore -->
```html
<!-- Total Whitespace: 20 -->
<section>###<h3>User profile</h3>###<label>#####User name#####<input>###</label>#</section>
```

Boʻshliqlarni shablonda yozilganidek saqlash koʻplab keraksiz [matn tugunlariga (text node)](https://developer.mozilla.org/en-US/docs/Web/API/Text) olib keladi va sahifani render qilish yukini oshiradi. Elementlar orasidagi bu boʻshliqlarni eʼtiborsiz qoldirish orqali Angular shablonni sahifada render qilishda kamroq ish bajaradi va umumiy unumdorlikni yaxshilaydi.

## Matn ichidagi qisqartiriladigan boʻshliqlar {#collapsible-whitespace-inside-text}

Veb-brauzeringiz HTML'ni sahifada render qilganda ketma-ket kelgan bir nechta boʻshliq belgisini bitta belgiga qisqartiradi:

<!-- prettier-ignore -->
```html
<!-- What it looks like in the template -->
<p>Hello         world</p>
```

Bu misolda brauzer "Hello" va "world" oʻrtasida faqat bitta boʻshliq koʻrsatadi.

```angular-html
<!-- What shows up in the browser -->
<p>Hello world</p>
```

Bu qanday ishlashi haqida koʻproq kontekst uchun [HTML, CSS va DOM'da boʻshliqlar qanday qayta ishlanadi](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Whitespace) maqolasiga qarang.

Angular shablonni kompilyatsiya qilishda bunday boʻshliqlarni bitta belgiga qisqartirib, bu keraksiz boʻshliq belgilarini brauzerga umuman yubormaslikka harakat qiladi.

## Boʻshliqlarni saqlash {#preserving-whitespace}

Shablon uchun `@Component` dekoratorida `preserveWhitespaces: true` koʻrsatib, Angular'ga shablondagi boʻshliqlarni saqlashni buyurishingiz mumkin.

```angular-ts
@Component({
  /* ... */,
  preserveWhitespaces: true,
  template: `
    <p>Hello         world</p>
  `
})
```

Mutlaqo zarur boʻlmasa, bu parametrni oʻrnatishdan qoching. Boʻshliqlarni saqlash Angular render qilishda sezilarli darajada koʻproq tugun hosil qilishiga va ilovangiz sekinlashishiga olib kelishi mumkin.

Bundan tashqari, Angular'ga xos maxsus HTML entity'si `&ngsp;`'dan foydalanishingiz mumkin. Bu entity kompilyatsiya qilingan natijada saqlanib qoladigan bitta boʻshliq belgisini hosil qiladi.
