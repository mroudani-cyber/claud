// Vortex Realm Discord assistant: AI help, tickets, polls, giveaways, tournaments, roles, welcome, announcements.
// Runs 24/7 with `node index.js`. Settings in .env (see .env.example). Data kept in data.json.
require('dotenv').config();
const fs = require('fs');
const path = require('path');
const {
  Client, GatewayIntentBits, Partials, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle,
  ChannelType, PermissionFlagsBits, SlashCommandBuilder, REST, Routes, AttachmentBuilder, Events,
} = require('discord.js');

const TOKEN = process.env.DISCORD_TOKEN;
const GUILD_ID = process.env.GUILD_ID || '1559180932592963586';
const GROQ_KEY = process.env.GROQ_API_KEY;
const GROQ_MODEL = process.env.GROQ_MODEL || 'openai/gpt-oss-120b';
const COLOR = 0x8B5CF6;
const SERVER_IP = process.env.SERVER_IP || 'vortexsmps.playwithbao.com';
const STAFF_ROLES = (process.env.STAFF_ROLE_IDS || [
  '1559459998080434196', '1560268551808483399', '1559460706451984425', '1559460059639976007', '1566464692791283924',
  '1559460666333601842', '1559460612667478056', '1559460159103701068', '1564737736835866686', '1559460822806306896', '1561127728856432840',
].join(',')).split(',').map(s => s.trim()).filter(Boolean);
// roles members can pick themselves (region and game)
const SELF_ROLES = {
  eu: '1564737448808947782', us: '1564737637988827357', asia: '1564737685434802246', africa: '1564737513753419986',
  pvp: '1564749049025003593', smp: '1564749112975429762',
};
const MEMBER_ROLE = process.env.MEMBER_ROLE_ID || '1559460271121236008';
// channels the assistant answers in without being mentioned
const AI_CHANNELS = (process.env.AI_CHANNELS || '🔍・questions,🤖・bot-commands').split(',');

// ------------------------------------------------------------------ data
const DATA_FILE = path.join(__dirname, 'data.json');
let data = { tickets: {}, polls: {}, giveaways: {}, tournaments: {}, ticketCount: 0 };
try { data = { ...data, ...JSON.parse(fs.readFileSync(DATA_FILE, 'utf8')) }; } catch { /* first start */ }
const save = () => fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMembers],
  partials: [Partials.Channel],
});

const isStaff = m => m && (m.permissions.has(PermissionFlagsBits.Administrator) || m.roles.cache.some(r => STAFF_ROLES.includes(r.id)));
const byName = (guild, name) => guild.channels.cache.find(c => c.name === name);
const embed = (title, desc) => new EmbedBuilder().setColor(COLOR).setTitle(title).setDescription(desc || null).setFooter({ text: 'Vortex Realm' }).setTimestamp();

// ------------------------------------------------------------------ AI
const SYSTEM = `You are "Vortex Assistant", the friendly helper of the Vortex Realm Minecraft Discord.
Server IP: ${SERVER_IP} (Java 1.21.11; Bedrock may not be supported). It is a practice PvP server with an SMP.
Features: ranked and unranked duels with tiers LT5 to HT1, 1.8 legacy kits (NoDebuff, Debuff, Gapple, Soup, Archer, Combo, BuildUHC, Classic),
FFA, practice bots, arcade (The Bridge, Sumo, Boxing, Spleef, OITC, KOTH, Parkour), parties, 2v2, clans, tournaments and a Weekly Cup,
battle pass, missions, achievements, cosmetics (/cosmetics: pets, wings, trims, sword skins), an SMP (/smp) with homes, tpa, rtp, warps, /kit,
seasons and its own Nether and End. Useful commands: /queue, /duel, /party, /ffa, /kiteditor, /cosmetics, /stats, /legacy, /arcade, /smp, /kit.
Help for staff applications: #📋・staff-applications. Support: open a ticket in #🎟️〢ticket. Rules: #📜・rules.
Rules for you: answer briefly (under 120 words), be kind and use simple English, never invent features, prices, or staff decisions;
if unsure say a staff member will help or suggest a ticket. Never ask for passwords or account details. Do not use @everyone or @here.`;

async function ai(messages, maxTokens = 400) {
  if (!GROQ_KEY) return 'The AI is not set up yet (no GROQ_API_KEY).';
  const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${GROQ_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: GROQ_MODEL, messages: [{ role: 'system', content: SYSTEM }, ...messages], max_tokens: maxTokens, temperature: 0.5 }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(j?.error?.message || `AI error ${r.status}`);
  return (j.choices?.[0]?.message?.content || '').trim().slice(0, 1900) || 'Sorry, I have no answer for that.';
}

const lastAsk = new Map();
client.on(Events.MessageCreate, async msg => {
  if (msg.author.bot || !msg.guild) return;
  const mentioned = msg.mentions.has(client.user);
  const inAiChannel = AI_CHANNELS.includes(msg.channel.name);
  const ticket = data.tickets[msg.channel.id];
  if (!mentioned && !inAiChannel && !(ticket && !ticket.aiOff && !isStaff(msg.member))) return;
  const now = Date.now();
  if (now - (lastAsk.get(msg.author.id) || 0) < 6000) return;
  lastAsk.set(msg.author.id, now);
  try {
    await msg.channel.sendTyping();
    const history = (await msg.channel.messages.fetch({ limit: 8 })).reverse()
      .filter(m => m.content)
      .map(m => ({ role: m.author.id === client.user.id ? 'assistant' : 'user', content: `${m.author.id === client.user.id ? '' : m.author.username + ': '}${m.content.replace(/<@!?\d+>/g, '').slice(0, 600)}` }));
    const answer = await ai(history);
    await msg.reply({ content: answer, allowedMentions: { parse: [], repliedUser: true } });
  } catch (e) {
    console.error('AI', e.message);
  }
});

// ------------------------------------------------------------------ welcome
client.on(Events.GuildMemberAdd, async member => {
  try {
    if (MEMBER_ROLE) await member.roles.add(MEMBER_ROLE).catch(() => {});
    const ch = byName(member.guild, '👋・welcome');
    if (ch) {
      await ch.send({ content: `${member}`, embeds: [embed('Welcome to Vortex Realm!', `Hey ${member}, welcome! 🎉\n\n**IP:** \`${SERVER_IP}\`\n📜 Read the rules, 🎭 pick your roles, and have fun!\nYou are member **#${member.guild.memberCount}**.`).setThumbnail(member.user.displayAvatarURL())] });
    }
  } catch (e) { console.error('welcome', e.message); }
});

// ------------------------------------------------------------------ slash commands
const commands = [
  new SlashCommandBuilder().setName('ask').setDescription('Ask the Vortex Assistant').addStringOption(o => o.setName('question').setDescription('Your question').setRequired(true)),
  new SlashCommandBuilder().setName('ip').setDescription('Server IP and how to join'),
  new SlashCommandBuilder().setName('ticket-panel').setDescription('Post the ticket panel (staff)'),
  new SlashCommandBuilder().setName('roles-panel').setDescription('Post the self-roles panel (staff)'),
  new SlashCommandBuilder().setName('poll').setDescription('Start a poll')
    .addStringOption(o => o.setName('question').setDescription('Question').setRequired(true))
    .addStringOption(o => o.setName('options').setDescription('Options separated by | (2-5)').setRequired(true))
    .addIntegerOption(o => o.setName('hours').setDescription('How long (default 24)')),
  new SlashCommandBuilder().setName('giveaway').setDescription('Start a giveaway or competition (staff)')
    .addStringOption(o => o.setName('prize').setDescription('Prize').setRequired(true))
    .addIntegerOption(o => o.setName('hours').setDescription('How long').setRequired(true))
    .addIntegerOption(o => o.setName('winners').setDescription('Number of winners (default 1)')),
  new SlashCommandBuilder().setName('tournament').setDescription('Tournaments')
    .addSubcommand(s => s.setName('create').setDescription('Open sign-ups (staff)')
      .addStringOption(o => o.setName('name').setDescription('Name, e.g. Sword 1v1 Cup').setRequired(true))
      .addIntegerOption(o => o.setName('size').setDescription('Max players (4, 8, 16, 32)').setRequired(true))
      .addStringOption(o => o.setName('prize').setDescription('Prize')))
    .addSubcommand(s => s.setName('start').setDescription('Close sign-ups and post the bracket (staff)'))
    .addSubcommand(s => s.setName('win').setDescription('Report a match winner (staff)').addUserOption(o => o.setName('player').setDescription('Winner').setRequired(true)))
    .addSubcommand(s => s.setName('bracket').setDescription('Show the bracket')),
  new SlashCommandBuilder().setName('rank').setDescription('Give or take a role (staff)')
    .addStringOption(o => o.setName('action').setDescription('give or remove').setRequired(true).addChoices({ name: 'give', value: 'give' }, { name: 'remove', value: 'remove' }))
    .addUserOption(o => o.setName('member').setDescription('Member').setRequired(true))
    .addRoleOption(o => o.setName('role').setDescription('Role').setRequired(true)),
  new SlashCommandBuilder().setName('announce').setDescription('Post an announcement (staff)')
    .addStringOption(o => o.setName('title').setDescription('Title').setRequired(true))
    .addStringOption(o => o.setName('text').setDescription('Text (use \\n for new lines)').setRequired(true))
    .addChannelOption(o => o.setName('channel').setDescription('Where (default announcements)'))
    .addBooleanOption(o => o.setName('ping').setDescription('Ping @everyone')),
].map(c => c.toJSON());

client.once(Events.ClientReady, async () => {
  console.log(`Online as ${client.user.tag}`);
  client.user.setActivity(`${SERVER_IP} | /ask`);
  try {
    await new REST({ version: '10' }).setToken(TOKEN).put(Routes.applicationGuildCommands(client.user.id, GUILD_ID), { body: commands });
    console.log('Slash commands ready');
  } catch (e) { console.error('commands', e.message); }
  setInterval(tickTimers, 30_000);
  tickTimers();
});

const staffOnly = async i => {
  if (isStaff(i.member)) return false;
  await i.reply({ content: 'Only staff can do that.', ephemeral: true });
  return true;
};

client.on(Events.InteractionCreate, async i => {
  try {
    if (i.isChatInputCommand()) return await onCommand(i);
    if (i.isButton()) return await onButton(i);
  } catch (e) {
    console.error('interaction', e);
    const r = { content: 'Something went wrong.', ephemeral: true };
    if (i.deferred || i.replied) i.followUp(r).catch(() => {}); else i.reply(r).catch(() => {});
  }
});

async function onCommand(i) {
  const g = i.guild;
  switch (i.commandName) {
    case 'ask': {
      await i.deferReply();
      const a = await ai([{ role: 'user', content: `${i.user.username}: ${i.options.getString('question')}` }]);
      return i.editReply({ content: a, allowedMentions: { parse: [] } });
    }
    case 'ip':
      return i.reply({ embeds: [embed('How to join', `**IP:** \`${SERVER_IP}\`\n**Version:** Java 1.21.11\n\nAdd the server in Multiplayer, join, and type \`/queue\` to play!`)] });
    case 'ticket-panel': {
      if (await staffOnly(i)) return;
      const row = new ActionRowBuilder().addComponents(
        new ButtonBuilder().setCustomId('tk:support').setLabel('Support').setEmoji('🎫').setStyle(ButtonStyle.Primary),
        new ButtonBuilder().setCustomId('tk:report').setLabel('Report a player').setEmoji('🚨').setStyle(ButtonStyle.Danger),
        new ButtonBuilder().setCustomId('tk:appeal').setLabel('Appeal').setEmoji('⚖️').setStyle(ButtonStyle.Secondary),
        new ButtonBuilder().setCustomId('tk:store').setLabel('Store').setEmoji('🛒').setStyle(ButtonStyle.Success),
      );
      await i.channel.send({ embeds: [embed('🎫 Vortex Support', 'Need help? Pick a button below and a private ticket opens for you.\n\n🎫 **Support:** questions and problems\n🚨 **Report:** cheaters, rule breakers\n⚖️ **Appeal:** banned or muted\n🛒 **Store:** purchases\n\nOur assistant answers right away; staff join soon after.')], components: [row] });
      return i.reply({ content: 'Panel posted.', ephemeral: true });
    }
    case 'roles-panel': {
      if (await staffOnly(i)) return;
      const r1 = new ActionRowBuilder().addComponents(
        ['eu', 'us', 'asia', 'africa'].map(k => new ButtonBuilder().setCustomId(`role:${k}`).setLabel(k.toUpperCase()).setEmoji('🌍').setStyle(ButtonStyle.Secondary)));
      const r2 = new ActionRowBuilder().addComponents(
        new ButtonBuilder().setCustomId('role:pvp').setLabel('PvP').setEmoji('⚔️').setStyle(ButtonStyle.Danger),
        new ButtonBuilder().setCustomId('role:smp').setLabel('SMP').setEmoji('🌲').setStyle(ButtonStyle.Success));
      await i.channel.send({ embeds: [embed('🎭 Pick your roles', 'Click to get a role, click again to remove it.\n\n🌍 **Region:** EU, US, Asia, Africa\n⚔️ **PvP** and 🌲 **SMP:** get pinged for what you play')], components: [r1, r2] });
      return i.reply({ content: 'Panel posted.', ephemeral: true });
    }
    case 'poll': {
      const opts = i.options.getString('options').split('|').map(s => s.trim()).filter(Boolean).slice(0, 5);
      if (opts.length < 2) return i.reply({ content: 'Give 2 to 5 options separated by |', ephemeral: true });
      const hours = Math.max(1, Math.min(168, i.options.getInteger('hours') || 24));
      const id = Date.now().toString(36);
      const poll = { id, q: i.options.getString('question'), opts, votes: {}, ends: Date.now() + hours * 3600_000, channel: i.channelId, message: null, by: i.user.id };
      const msg = await i.reply({ embeds: [pollEmbed(poll)], components: pollRows(poll), fetchReply: true });
      poll.message = msg.id; data.polls[id] = poll; save();
      return;
    }
    case 'giveaway': {
      if (await staffOnly(i)) return;
      const hours = Math.max(1, Math.min(720, i.options.getInteger('hours')));
      const id = Date.now().toString(36);
      const gw = { id, prize: i.options.getString('prize'), winners: Math.max(1, Math.min(10, i.options.getInteger('winners') || 1)), ends: Date.now() + hours * 3600_000, entries: [], channel: i.channelId, message: null };
      const row = new ActionRowBuilder().addComponents(new ButtonBuilder().setCustomId(`gw:${id}`).setLabel('Enter').setEmoji('🎉').setStyle(ButtonStyle.Success));
      const msg = await i.reply({ embeds: [giveawayEmbed(gw)], components: [row], fetchReply: true });
      gw.message = msg.id; data.giveaways[id] = gw; save();
      return;
    }
    case 'tournament': return onTournament(i);
    case 'rank': {
      if (await staffOnly(i)) return;
      const member = await g.members.fetch(i.options.getUser('member').id);
      const role = i.options.getRole('role');
      const me = g.members.me;
      if (role.position >= me.roles.highest.position || role.managed) return i.reply({ content: 'I can\'t manage that role (it is above mine or belongs to a bot).', ephemeral: true });
      if (role.position >= i.member.roles.highest.position && g.ownerId !== i.user.id) return i.reply({ content: 'You can only manage roles below your own.', ephemeral: true });
      if (i.options.getString('action') === 'give') await member.roles.add(role, `by ${i.user.tag}`); else await member.roles.remove(role, `by ${i.user.tag}`);
      const log = byName(g, '📜・staff-actions');
      if (log) log.send({ embeds: [embed('Role change', `${i.user} **${i.options.getString('action')}** ${role} → ${member}`)] }).catch(() => {});
      return i.reply({ content: `Done: ${i.options.getString('action')} ${role.name} for ${member.user.username}.`, ephemeral: true });
    }
    case 'announce': {
      if (await staffOnly(i)) return;
      const ch = i.options.getChannel('channel') || byName(g, '📢・announcements') || i.channel;
      const ping = i.options.getBoolean('ping');
      await ch.send({ content: ping ? '@everyone' : undefined, embeds: [embed(i.options.getString('title'), i.options.getString('text').replace(/\\n/g, '\n'))], allowedMentions: { parse: ping ? ['everyone'] : [] } });
      return i.reply({ content: `Posted in ${ch}.`, ephemeral: true });
    }
  }
}

// ------------------------------------------------------------------ buttons
async function onButton(i) {
  const [kind, arg] = i.customId.split(':');
  const g = i.guild;
  if (kind === 'role') {
    const id = SELF_ROLES[arg];
    if (!id) return;
    const has = i.member.roles.cache.has(id);
    if (has) await i.member.roles.remove(id); else await i.member.roles.add(id);
    return i.reply({ content: `${has ? 'Removed' : 'Added'} the ${arg.toUpperCase()} role.`, ephemeral: true });
  }
  if (kind === 'tk') {
    const open = Object.entries(data.tickets).find(([, t]) => t.owner === i.user.id && !t.closed);
    if (open && g.channels.cache.get(open[0])) return i.reply({ content: `You already have a ticket: <#${open[0]}>`, ephemeral: true });
    const cat = g.channels.cache.find(c => c.type === ChannelType.GuildCategory && c.name.includes('SUPPORT'));
    data.ticketCount++;
    const ch = await g.channels.create({
      name: `ticket-${String(data.ticketCount).padStart(4, '0')}-${i.user.username}`.slice(0, 90),
      type: ChannelType.GuildText,
      parent: cat?.id,
      permissionOverwrites: [
        { id: g.roles.everyone.id, deny: [PermissionFlagsBits.ViewChannel] },
        { id: i.user.id, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.AttachFiles, PermissionFlagsBits.ReadMessageHistory] },
        { id: client.user.id, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.ManageChannels] },
        ...STAFF_ROLES.filter(r => g.roles.cache.has(r)).map(r => ({ id: r, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages, PermissionFlagsBits.ReadMessageHistory] })),
      ],
    });
    data.tickets[ch.id] = { owner: i.user.id, type: arg, opened: Date.now() };
    save();
    const row = new ActionRowBuilder().addComponents(
      new ButtonBuilder().setCustomId('tkclose:x').setLabel('Close').setEmoji('🔒').setStyle(ButtonStyle.Danger),
      new ButtonBuilder().setCustomId('tkstaff:x').setLabel('Talk to staff only').setEmoji('🙋').setStyle(ButtonStyle.Secondary));
    const tips = { support: 'Tell us what is wrong and your Minecraft name.', report: 'Who, what they did, when, and proof (video or screenshots).', appeal: 'Your Minecraft name, the punishment, and why it should be removed.', store: 'Your Minecraft name, what you bought, and the transaction ID.' };
    await ch.send({ content: `${i.user}`, embeds: [embed(`🎫 ${arg[0].toUpperCase() + arg.slice(1)} ticket`, `Thanks for opening a ticket!\n\n${tips[arg] || ''}\n\nThe assistant can answer simple questions right away. Press **Talk to staff only** to turn it off.`)], components: [row] });
    return i.reply({ content: `Your ticket: ${ch}`, ephemeral: true });
  }
  if (kind === 'tkstaff') {
    const t = data.tickets[i.channelId];
    if (t) { t.aiOff = true; save(); }
    return i.reply({ content: 'Got it, a staff member will answer you here.' });
  }
  if (kind === 'tkclose') {
    const t = data.tickets[i.channelId];
    if (!t) return i.reply({ content: 'Not a ticket.', ephemeral: true });
    if (t.owner !== i.user.id && !isStaff(i.member)) return i.reply({ content: 'Only the owner or staff can close it.', ephemeral: true });
    await i.reply('Closing in 5 seconds and saving a transcript...');
    const msgs = (await i.channel.messages.fetch({ limit: 100 })).reverse();
    const text = msgs.map(m => `[${new Date(m.createdTimestamp).toISOString()}] ${m.author.username}: ${m.content}${m.embeds.length ? ' [embed]' : ''}`).join('\n');
    const log = byName(g, '🧾・ticket-transcripts');
    if (log) await log.send({ embeds: [embed('Ticket closed', `**${i.channel.name}**\nOpened by <@${t.owner}> • ${t.type}\nClosed by ${i.user}`)], files: [new AttachmentBuilder(Buffer.from(text), { name: `${i.channel.name}.txt` })] }).catch(() => {});
    t.closed = Date.now(); save();
    setTimeout(() => i.channel.delete('Ticket closed').catch(() => {}), 5000);
    return;
  }
  if (kind === 'poll') {
    const [pid, idx] = arg.split('.');
    const poll = data.polls[pid];
    if (!poll || poll.done) return i.reply({ content: 'This poll is over.', ephemeral: true });
    poll.votes[i.user.id] = Number(idx); save();
    await i.update({ embeds: [pollEmbed(poll)], components: pollRows(poll) });
    return;
  }
  if (kind === 'gw') {
    const gw = data.giveaways[arg];
    if (!gw || gw.done) return i.reply({ content: 'This giveaway is over.', ephemeral: true });
    if (gw.entries.includes(i.user.id)) { gw.entries = gw.entries.filter(x => x !== i.user.id); save(); return i.reply({ content: 'You left the giveaway.', ephemeral: true }); }
    gw.entries.push(i.user.id); save();
    await i.message.edit({ embeds: [giveawayEmbed(gw)] }).catch(() => {});
    return i.reply({ content: 'You are in! Good luck 🍀', ephemeral: true });
  }
  if (kind === 'tj') {
    const t = data.tournaments.current;
    if (!t || t.started) return i.reply({ content: 'Sign-ups are closed.', ephemeral: true });
    if (t.players.includes(i.user.id)) { t.players = t.players.filter(x => x !== i.user.id); save(); return i.reply({ content: 'You left the tournament.', ephemeral: true }); }
    if (t.players.length >= t.size) return i.reply({ content: 'The tournament is full.', ephemeral: true });
    t.players.push(i.user.id); save();
    await i.message.edit({ embeds: [tourneyEmbed(t)] }).catch(() => {});
    return i.reply({ content: `You joined **${t.name}**! Be online in-game when it starts.`, ephemeral: true });
  }
}

// ------------------------------------------------------------------ polls and giveaways
const bar = (n, total) => '█'.repeat(total ? Math.round(n / total * 12) : 0).padEnd(12, '░');
function pollEmbed(p) {
  const counts = p.opts.map((_, k) => Object.values(p.votes).filter(v => v === k).length);
  const total = counts.reduce((a, b) => a + b, 0);
  return embed(`📊 ${p.q}`, p.opts.map((o, k) => `**${k + 1}. ${o}**\n\`${bar(counts[k], total)}\` ${counts[k]} (${total ? Math.round(counts[k] / total * 100) : 0}%)`).join('\n\n')
    + `\n\n${p.done ? '**Poll closed.**' : `Ends <t:${Math.floor(p.ends / 1000)}:R> • ${total} votes`}`);
}
const pollRows = p => p.done ? [] : [new ActionRowBuilder().addComponents(p.opts.map((o, k) => new ButtonBuilder().setCustomId(`poll:${p.id}.${k}`).setLabel(`${k + 1}. ${o}`.slice(0, 80)).setStyle(ButtonStyle.Primary)))];
const giveawayEmbed = gw => embed(`🎉 ${gw.prize}`, `${gw.done ? `**Winners:** ${gw.winnerIds?.length ? gw.winnerIds.map(x => `<@${x}>`).join(', ') : 'nobody entered'}` : `Click **Enter** to join!\nEnds <t:${Math.floor(gw.ends / 1000)}:R>`}\n\n**Winners:** ${gw.winners} • **Entries:** ${gw.entries.length}`);

async function tickTimers() {
  const now = Date.now();
  for (const p of Object.values(data.polls)) {
    if (!p.done && now >= p.ends) {
      p.done = true; save();
      const ch = await client.channels.fetch(p.channel).catch(() => null);
      const m = ch && await ch.messages.fetch(p.message).catch(() => null);
      if (m) m.edit({ embeds: [pollEmbed(p)], components: [] }).catch(() => {});
    }
  }

  for (const gw of Object.values(data.giveaways)) {
    if (!gw.done && now >= gw.ends) {
      const pool = [...gw.entries];
      gw.winnerIds = [];
      while (pool.length && gw.winnerIds.length < gw.winners) gw.winnerIds.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
      gw.done = true; save();
      const ch = await client.channels.fetch(gw.channel).catch(() => null);
      if (!ch) continue;
      const m = await ch.messages.fetch(gw.message).catch(() => null);
      if (m) m.edit({ embeds: [giveawayEmbed(gw)], components: [] }).catch(() => {});
      ch.send(gw.winnerIds.length ? `🎉 Congratulations ${gw.winnerIds.map(x => `<@${x}>`).join(', ')}! You won **${gw.prize}**. Open a ticket to claim it.` : `Nobody entered the giveaway for **${gw.prize}**.`).catch(() => {});
    }
  }
}

// ------------------------------------------------------------------ tournaments (single elimination)
const tourneyEmbed = t => embed(`🏆 ${t.name}`, `${t.prize ? `**Prize:** ${t.prize}\n` : ''}**Players:** ${t.players.length}/${t.size}\n${t.players.map(x => `<@${x}>`).join(', ') || 'Nobody yet'}\n\n${t.started ? '' : 'Click **Join** to sign up!'}`);
function bracketText(t) {
  return t.rounds.map((r, n) => `**Round ${n + 1}**\n` + r.map(m => `${m.a ? `<@${m.a}>` : 'BYE'} vs ${m.b ? `<@${m.b}>` : 'BYE'}${m.w ? ` → 🏅 <@${m.w}>` : ''}`).join('\n')).join('\n\n');
}
function advance(t) {
  const r = t.rounds[t.rounds.length - 1];
  r.forEach(m => { if (!m.w && (!m.a || !m.b)) m.w = m.a || m.b; });
  if (r.every(m => m.w)) {
    const winners = r.map(m => m.w);
    if (winners.length === 1) { t.champion = winners[0]; return; }
    const next = [];
    for (let k = 0; k < winners.length; k += 2) next.push({ a: winners[k], b: winners[k + 1] || null });
    t.rounds.push(next);
    advance(t);
  }
}

async function onTournament(i) {
  const sub = i.options.getSubcommand();
  const t = data.tournaments.current;
  if (sub === 'bracket') {
    if (!t || !t.started) return i.reply({ content: 'No bracket yet.', ephemeral: true });
    return i.reply({ embeds: [embed(`🏆 ${t.name}: bracket`, bracketText(t) + (t.champion ? `\n\n👑 **Champion:** <@${t.champion}>` : ''))] });
  }

  if (await staffOnly(i)) return;
  if (sub === 'create') {
    const size = [4, 8, 16, 32].includes(i.options.getInteger('size')) ? i.options.getInteger('size') : 16;
    data.tournaments.current = { name: i.options.getString('name'), size, prize: i.options.getString('prize') || '', players: [], started: false, rounds: [] };
    save();
    const row = new ActionRowBuilder().addComponents(new ButtonBuilder().setCustomId('tj:x').setLabel('Join').setEmoji('⚔️').setStyle(ButtonStyle.Success));
    const ch = byName(i.guild, '🏟️・tournaments') || i.channel;
    await ch.send({ embeds: [tourneyEmbed(data.tournaments.current)], components: [row] });
    return i.reply({ content: `Sign-ups open in ${ch}.`, ephemeral: true });
  }

  if (!t) return i.reply({ content: 'No tournament. Use /tournament create first.', ephemeral: true });
  if (sub === 'start') {
    if (t.players.length < 2) return i.reply({ content: 'Need at least 2 players.', ephemeral: true });
    const shuffled = [...t.players].sort(() => Math.random() - 0.5);
    let n = 1;
    while (n < shuffled.length) n *= 2;
    while (shuffled.length < n) shuffled.push(null);
    const first = [];
    for (let k = 0; k < n; k += 2) first.push({ a: shuffled[k], b: shuffled[k + 1] });
    t.rounds = [first]; t.started = true; advance(t); save();
    return i.reply({ embeds: [embed(`🏆 ${t.name} has started!`, bracketText(t))] });
  }

  if (sub === 'win') {
    const w = i.options.getUser('player').id;
    const r = t.rounds[t.rounds.length - 1];
    const m = r.find(x => !x.w && (x.a === w || x.b === w));
    if (!m) return i.reply({ content: 'That player has no open match.', ephemeral: true });
    m.w = w; advance(t); save();
    if (t.champion) {
      const done = embed(`👑 ${t.name}: champion`, `Congratulations <@${t.champion}>!${t.prize ? `\n**Prize:** ${t.prize}` : ''}\n\n${bracketText(t)}`);
      data.tournaments.current = null; save();
      return i.reply({ embeds: [done] });
    }
    return i.reply({ embeds: [embed(`🏆 ${t.name}`, bracketText(t))] });
  }
}

if (!TOKEN) {
  console.error('Set DISCORD_TOKEN in .env first.');
  process.exit(1);
}

client.login(TOKEN);
