# Tasks: add-doxchat-model-intake

## 1. Arrival

- [x] 1.1 The delta is carried byte-identical from the openxFactory packet, and
      the source is named so the check can be repeated after `main` moves:
      `opensoft/openxFactory`
      `openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md`
      at `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
      `3de54f7ee6f24f890d8e305914b592340b53d274`, 16,813 bytes,
      `sha256 3168ad8f6f31c8dbacdc772d933508943f7b2c7cf373de2357eb8958d4bebee1`.
      `git hash-object` reads that same blob id over this repository's copy, so
      the two files are one git object rather than two that agree. The
      openxFactory packet is closed as re-homed in the same window.
- [ ] 1.2 The capability `ideation-dashboard` reaches this corpus with
      `split-opendox-two-layer-product` § 5's shed — pinned, because the
      condition that blocks archiving must stay checkable after `main` moves:
      `opensoft/openxFactory`
      `openspec/changes/split-opendox-two-layer-product/tasks.md` at
      `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
      `a3470096010d7279b38011e02cefaaada1d7b88f` (114,414 bytes), § 5 at line
      1095, *"openxFactory consumes and sheds; the MAJOR is cut. BREAKING"*.
      **Until it does, this change cannot archive** — `openspec validate
      --strict` passes and reports "Archive would refuse this delta: target spec
      does not exist".
- [ ] 1.3 **Re-verify the MODIFIED block against openDox's canon before
      archiving.** The delta's own preamble asks for this against openxFactory's
      canon; the re-home moves the referent, and the instruction is carried out
      of prose into a box so it is not re-read as satisfied.
- [ ] 1.4 This change's standing in THIS corpus is openDox's own act. The text
      arrives ratified in openxFactory (Brett Heap, 2026-08-21) and
      `Status: draft` here until openDox ratifies it.

## 2. The realization that travelled with it

Twenty-one of the openxFactory packet's boxes were ticked there; the code moves
with the carve into `opensoft/openDox-code` rather than being rebuilt.

- [ ] 2.1 Re-verify the built surfaces against `openDox-code` after the carve
      lands there. **NOT "the same code" — the same code MODULO DECLARED EDITS,
      and the distinction decides what the re-verification is for.** They are
      ticked on the openxFactory evidence, but § 6.3 of the split packet's ledger
      (`opensoft/openxFactory`
      `openspec/changes/split-opendox-two-layer-product/tasks.md` at
      `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
      `a3470096010d7279b38011e02cefaaada1d7b88f`, line 1502) says this packet's
      code moves "as `moved_with_declared_edit` rows", and `proposal.md`'s Impact
      section says the same. A declared edit changes the moved bytes, so the
      openxFactory ticks are evidence about the PRE-CARVE tree. The
      re-verification is therefore owed twice over: because the four-part floor
      proves test counts per destination rather than inheriting them, and because
      the post-carve behaviour is not guaranteed identical to the behaviour those
      ticks were taken against. Treating the source evidence as evidence for
      unchanged bytes is the specific error this box exists to prevent.

## 3. What was still open when it moved, carried OPEN

- [ ] 3.1 **Live-console proof on the real serve.** Carried open from the
      openxFactory packet's § 4.1, where it was open "honestly".
- [ ] 3.2 **Realization evidence recorded.** Carried open from § 4.2. The
      evidence discipline is openDox's own once the code leg holds the code;
      openxFactory's `release-realization` governs openxFactory's corpus.

## 4. What did NOT travel

- [x] 4.1 The additive `action` enum member is ALREADY openxFactory contract
      bytes at the published tag and STAYS there. Both halves pinned, so the
      decision is reproducible evidence rather than an assertion about why a file
      is absent here:
      **the bytes** — `opensoft/openxFactory`
      `contracts/schemas/gate-action-record.schema.yaml` at tag `contract-v1.45`
      (commit `7b7447da8f769c2884d7586959e5fecb4b6eeb00`), blob
      `7f95006f768fbc2f4422d49642ba5ca0afbbac7f`, 45,078 bytes — PRESENT there,
      **ABSENT at `cb2d3a2c` and on today's openxFactory `main`** (measured
      2026-09-16; a filename search over that repository returns zero), which is
      why the tag is the only reference that can carry this claim;
      **the decision** — § 6.3 of `openspec/changes/split-opendox-two-layer-product/tasks.md`
      at `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
      `a3470096010d7279b38011e02cefaaada1d7b88f`, line 1502: *"its one additive
      schema enum member is already `openxFactory` contract bytes and STAYS."*
      Recorded as a decision, not an omission.

## 5. Readings registered at arrival, NOT applied to the carried text

RULING Q6 freezes this packet where it stands and § 6.3 carries its delta
**byte-identical** — `sha256 3168ad8f…`, 16,813 bytes, `diff`-verified against
the archived copy in openxFactory. That equality is the closure's own evidence
on openxFactory PR #1057, so a reading of the TEXT cannot be answered by editing
the text here without falsifying the act. It is recorded instead, against the
ratification this corpus still owes (§ 1.4).

- [x] 5.1 **ANSWERED from the delta's own text, no change owed.** Copilot,
      reviewing openDox-spec #13 at `9925fd0`, read *"The model selector SHALL
      render its intake affordance as the FIRST option … and SHALL make it the
      DEFAULT selection when the catalog discloses no available entry"* as an
      UNCONDITIONAL rule contradicting two others: the affordance is *"not
      rendered at all"* when the broker this flow requires is unavailable, and
      *"MUST be absent"* on the hosted plane. The three do not collide, and the
      delta says why in terms:
      **whether the affordance EXISTS is one question and WHERE IT SITS is
      another.** *The intake affordance ships with the flow behind it* governs
      existence — *"Where the flow's dependencies are not yet met, the selector
      SHALL keep its present behaviour unchanged rather than showing a disabled
      or explanatory intake option"* — and the hosted-plane scenario governs it
      again, for the stated reason that *"a plane that may not run a turn may not
      enrol a provider either"*. The ordering-and-default rule speaks to the
      selector that HAS the affordance. An empty catalog with no broker is
      therefore not a case with two outcomes: there is no affordance to order,
      and the selector keeps the behaviour it has today.
      The delta also draws the neighbouring distinction the reading might have
      collapsed into this one: an UNREADABLE catalog is not an empty one, and
      intake *"MUST NOT be offered when the catalog could not be READ"*.

**5.2 — AVAILABLE, NOT OWED, AND DELIBERATELY NOT A BOX.** If openDox wants the
precedence stated in terms rather than derived, that is a ratification-time
amendment in THIS corpus (§ 1.4), not an arrival edit: one sentence in the
ordering requirement naming the existence rule as its precondition. The text is
already consistent, and a re-home is not the act that rewrites what openxFactory
ratified.

It carried a `- [ ]` until Copilot's reading of openDox-spec #13, which is right:
in a task ledger an unticked box reports outstanding work, and nothing here is
owed. Ticking it would have been worse — that claims an amendment was made. So it
leaves the checklist entirely and stays a note, where neither a reader nor task
tooling can count an option as an obligation. The number is kept so that
references to § 5.2 still resolve.

- [ ] 5.3 **THE CREDENTIAL BAN AND THE INTAKE FLOW READ AS A CONTRADICTION, and
      the resolving distinction is not in the text.** The catalog requirement
      says provider credentials *"MUST NOT enter browser storage, a request body,
      response body, dashboard snapshot, chat transcript, thread file, log, gate
      record, git artifact, or exception detail"*; the intake requirement says an
      intake flow *"SHALL pass the supplied value directly to the declared
      credential broker"*, with a scenario that begins *"WHEN a key is entered in
      the intake flow"*. A key a human types in the browser reaches the broker
      through a request body or it does not reach it at all, so read flatly the
      two cannot both be satisfied and no conforming implementation can support
      the API-key path the change exists to add.
      **THE READING THAT RESOLVES THEM is INGESTION versus STEADY STATE**: the
      ban governs a credential the SERVER holds and uses — which "MUST come only
      from the deployment's approved server-side credential mechanism", the
      clause the enumeration attaches to — while intake is the act that CREATES
      such a credential, whose one-way passage to the broker the intake
      requirement then constrains far more tightly than the ban does (no file, no
      state outliving the request, no echo, no log, no snapshot). On that reading
      the intake path is the single declared exception and everything after it is
      a broker reference rather than a secret.
      **BUT THAT IS A READING, NOT THE TEXT**, and a reader who does not reach
      for it is left with a flat prohibition that forbids the flow. **§ 1.4's
      business** — openDox's own ratification either narrows the ban to
      provider/model request bodies or names the broker handoff as the permitted
      ingestion channel in terms. Registered rather than applied: RULING Q6
      carries this delta byte-identical, and openxFactory PR #1057 states that
      carriage as a `sha256` equality over **the carried delta** —
      `specs/ideation-dashboard/spec.md`, blob
      `3de54f7ee6f24f890d8e305914b592340b53d274`, 16,813 bytes. **CORRECTED
      2026-09-16:** this sentence previously said "over every file of the
      packet", which overclaimed the evidence in a ledger whose whole subject is
      what the evidence covers. It does not: `proposal.md` and this file are
      RE-AUTHORED in this corpus, and `proposal.md`'s "What changes" section
      scopes the digest to the one file explicitly.
      **RE-RAISED at `4c2d4b9c`, and the registration is unchanged.** The review
      restated the contradiction from the requirement's own side — a server
      cannot receive a browser-entered value without a request payload — and
      asked for a security decision before ratification or implementation. That
      is this box, and the two ways out it already names are the two the review
      names. It is recorded here so a later round does not read it as new: the
      only thing that would change this box is openDox's ratification act
      (§ 1.4), and no arrival edit can stand in for it without falsifying the
      byte-identical carriage that is this closure's evidence.
