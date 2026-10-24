# Inyeksiya qilinadigan servis yaratish

Angular'da bogʻliqliklarni inyeksiya qilish (DI) — freymvorkning eng kuchli xususiyatlaridan biri. Bogʻliqliklarni inyeksiya qilishni Angular'ning ilovangiz uchun kerakli resurslarni ish vaqtida (runtime) _taqdim etish_ qobiliyati deb hisoblang. Bogʻliqlik servis yoki boshqa biror resurs boʻlishi mumkin.

NOTE: [Asoslar qoʻllanmasida bogʻliqliklarni inyeksiya qilish](/essentials/dependency-injection) haqida koʻproq bilib oling.

Bu mashgʻulotda `injectable` (inyeksiya qilinadigan) servisni qanday yaratishni oʻrganasiz.

<hr>

Servisdan foydalanish usullaridan biri — maʼlumotlar va API'lar bilan oʻzaro aloqa vositasi boʻlib xizmat qilish. Servisni qayta ishlatiladigan qilish uchun mantiqni servisda saqlashingiz va kerak boʻlganda uni ilova boʻylab ulashishingiz kerak.

Klassni DI tizimi tomonidan inyeksiya qilinishi mumkin boʻlgan qilish uchun `@Service` dekoratoridan foydalaning. Masalan:

```ts {highlight:[1]}
@Service()
class UserService {
  // methods to retrieve and return data
}
```

`@Service` dekoratori klassni servis sifatida belgilaydi va DI tizimiga `UserService`'ga ilovangizning istalgan joyidan murojaat qilish mumkinligini bildiradi. Sukut boʻyicha Angular servisni butun ilovangiz boʻylab taqdim etadi, shuning uchun qoʻshimcha konfiguratsiya yozishingiz shart emas.

NOTE: Sukut boʻyicha `@Service` klassni ildiz injector'da taqdim etadi. Agar uni qoʻlda taqdim etmoqchi boʻlsangiz, masalan, uni muayyan marshrut yoki komponent doirasi bilan cheklash uchun, `autoProvided: false` qiymatini oʻrnating. [Servislarni yaratish va ishlatish boʻyicha qoʻllanmada](guide/di/creating-and-using-services#using-the-service-vs-injectable-decorator) koʻproq bilib oling.

Xoʻsh, endi oʻzingiz sinab koʻring:

<docs-workflow>

<docs-step title="`@Service` dekoratorini qoʻshing {#add-the-service-decorator}">
`car.service.ts` faylidagi kodni `CarService` klassiga `@Service()` dekoratorini qoʻshish orqali yangilang.

TIP: Toʻgʻri sintaksisni topish uchun yuqoridagi misoldan foydalaning.

</docs-step>

</docs-workflow>

Barakalla 👍 endi bu servis `injectable` boʻldi va oʻyinga qoʻshilishi mumkin. Servis `injectable` boʻlgani uchun, keling, uni komponentga inyeksiya qilib koʻramiz 👉
