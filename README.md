<h1 align="center">Angular hujjatlari — Oʻzbekcha 🇺🇿</h1>

<p align="center">
  <img src="adev/src/assets/images/press-kit/angular_icon_gradient.gif" alt="angular-logo" height="120px" align="middle"/>
  <br>
  <em>Angular rasmiy hujjatlarining jamoa tomonidan yuritiladigan oʻzbekcha tarjimasi.</em>
  <br>
</p>

<p align="center">
  <a href="https://angular.dev/"><strong>angular.dev</strong></a>
  ·
  <a href="https://github.com/angular/angular"><strong>angular/angular</strong></a>
</p>

<hr>

## Loyiha haqida

Bu repozitoriy Angular rasmiy hujjatlarining (`adev`) oʻzbek tiliga (lotin yozuvi) tarjimasini saqlaydi.
Maqsad — angular.dev saytidagi "Community translations" roʻyxatiga qoʻshiladigan toʻlaqonli oʻzbekcha sayt yaratish.

- **Asos:** Angular **v22** (`main` tarmogʻi bilan muntazam sinxronlanadi)
- **Manba:** `adev/src/content` ostidagi rasmiy Angular hujjatlari
- **Tarjima tarmogʻi:** `uzbek-doc` (asosiy tarmoq). `main` tarmogʻi upstream bilan bir xil saqlanadi.

## Holat

| Boʻlim | Holat |
|---|---|
| Kirish → Angular nima? | ✅ tarjima qilingan |
| Kirish → Oʻrnatish | ✅ tarjima qilingan |
| Kirish → Asoslar → Umumiy koʻrinish | ✅ tarjima qilingan |
| Asoslar (komponentlar, signallar, shablonlar, signal formalar, DI, keyingi qadamlar) | ✅ tarjima qilingan |
| Chuqur qoʻllanmalar → Komponentlar (13 sahifa) | ✅ tarjima qilingan |
| Bosh sahifa, navigatsiya, footer | ✅ tarjima qilingan |
| Chuqur qoʻllanmalar → qolganlari (`guide/`) | ⏳ navbatda |
| Darsliklar (`tutorials/`) | ⏳ navbatda |

## Hissa qoʻshish

Imlo xatosi topdingizmi, jumlani ravonroq qila olasizmi yoki biror sahifani tarjima qilmoqchimisiz? Hissangizni kutamiz.

1. Repozitoriyni fork qiling
2. `adev/src/content/**/*.md` ostidagi kerakli fayllarni tahrirlang (`uzbek-doc` tarmogʻida)
3. Pull request oching

Tarjima qoidalari:

- Lotin yozuvidagi oʻzbek tili. Oʻ va gʻ uchun `ʻ` (U+02BB) belgisidan foydalaning: *oʻrnatish*, *bogʻliqlik*.
- Kod bloklari, `<docs-*>` teglari, `href`, `imgSrc` va boshqa atributlar oʻzgartirilmaydi — faqat koʻrinadigan matn tarjima qilinadi.
- Umumiy qabul qilingan texnik atamalar (component, signal, template, dependency injection) birinchi marta uchraganda oʻzbekcha izoh bilan, keyin inglizcha holda qoldiriladi.
- Sahifa sarlavhalari uchun `adev/src/app/routing/navigation-entries/index.ts` dagi `label` qiymatlarini ham yangilang.
- Har bir tarjima qilingan sarlavhaga inglizcha asl id'ni qoʻshing, aks holda saytdagi ichki havolalar buziladi va build muvaffaqiyatsiz boʻladi: `## Dinamik matnni koʻrsatish {#showing-dynamic-text}`.

## Upstream bilan sinxronlash

```shell
git fetch upstream
git checkout main && git merge --ff-only upstream/main && git push origin main
git checkout uzbek-doc && git merge main
# ziddiyatlarni hal qiling, tarjimalarni yangilang, soʻng:
git push origin uzbek-doc
```

## Lokal ishga tushirish

Angular repozitoriysidagi `adev/README.md` koʻrsatmalariga amal qiling (pnpm + Bazel).

## Litsenziya

Angular bilan bir xil — MIT. Qarang: [LICENSE](LICENSE).
