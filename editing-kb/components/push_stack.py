"""Push-down caption stack for Refract add_motion_html.
Lines enter word-by-word (blur-in); each new line lifts the stack with a spring overshoot;
older lines dim and shrink; a slam word squashes with a camera shake; a payoff rises from a mask.
CSS keyframes always end with a 100% hold (otherwise CSS springs back to the start state)."""
def build(D, stackA, stackB, slam_t, accent='#F2C14E', top='57%'):
    p=lambda s:f"{min(s,D)/D*100:.2f}%"
    def kf(name,frames):
        frames=frames+[(D,frames[-1][1])]
        return f"@keyframes {name}{{"+''.join(f"{p(t)}{{{v}}}" for t,v in frames)+"}"
    def words(txt,d0): return ''.join(f'<span class="w" style="animation-delay:{d0+i*0.07:.2f}s">{w}&nbsp;</span>' for i,w in enumerate(txt.split()))
    def lift(name,entries):
        fr=[(0,'transform:translateY(0)')];y=0
        for t,dy in entries:
            fr+= [(t,f'transform:translateY({y}px)'),(t+0.22,f'transform:translateY({y-dy-12}px)'),(t+0.35,f'transform:translateY({y-dy}px)')];y-=dy
        return kf(name,fr)
    A_lines,A_lift,A_out=stackA; B_lines,B_lift=stackB
    css=f"""@import url('https://fonts.googleapis.com/css2?family=Anton&family=Playfair+Display:ital,wght@1,700&family=Montserrat:wght@600;800&display=swap');
.cam{{position:absolute;inset:0;perspective:1600px;animation:cam {D}s cubic-bezier(.45,0,.55,1) both}}
.stage{{position:absolute;left:8%;right:8%;top:{top};transform-style:preserve-3d;transform:rotateX(8deg) rotateY(-6deg)}}
.A{{position:absolute;left:0;top:0;width:100%;animation:liftA {D}s linear both}} .Ao{{animation:outA {D}s linear both}}
.B{{position:absolute;left:0;top:0;width:100%;animation:liftB {D}s linear both}}
.ln{{position:absolute;left:0;white-space:nowrap;transform-origin:0 50%}}
.w{{display:inline-block;opacity:0;filter:blur(8px);animation:win .16s cubic-bezier(.16,1,.3,1) forwards}}
.s{{font-family:Montserrat;font-weight:600;font-size:54px;color:#F4EFE6;text-shadow:0 4px 18px rgba(0,0,0,.65)}}
.g{{font-family:Anton;font-size:190px;line-height:1;color:{accent};text-shadow:0 10px 40px rgba(0,0,0,.55),0 0 30px {accent}40}}
.i{{font-family:'Playfair Display';font-style:italic;font-weight:700;font-size:150px;line-height:1;color:#F4EFE6;text-shadow:0 10px 40px rgba(0,0,0,.6)}}
@keyframes win{{to{{opacity:1;filter:blur(0)}}}}
{lift('liftA',A_lift)}{lift('liftB',B_lift)}
{kf('outA',[(0,'opacity:1;filter:blur(0)'),(A_out,'opacity:1;filter:blur(0)'),(A_out+0.16,'opacity:0;filter:blur(10px)')])}
{kf('cam',[(0,'transform:scale(1) translate(0,0)'),(slam_t-0.1,'transform:scale(1.03) translate(-6px,4px)'),(slam_t+0.04,'transform:scale(1.05) translate(10px,-8px)'),(slam_t+0.08,'transform:scale(1.04) translate(-8px,6px)'),(slam_t+0.13,'transform:scale(1.035) translate(4px,-3px)'),(slam_t+0.2,'transform:scale(1.03) translate(0,0)'),(D,'transform:scale(1.06) translate(6px,-4px)')])}
.slam{{opacity:0;animation:slam .42s {slam_t}s cubic-bezier(.34,1.56,.64,1) forwards}}
@keyframes slam{{0%{{opacity:0;transform:scale(1.6);filter:blur(14px)}}35%{{opacity:1;transform:scale(.96,1.05);filter:blur(0)}}65%{{opacity:1;transform:scale(1.03,.98)}}100%{{opacity:1;transform:scale(1)}}}}
.rise{{opacity:0;transform:translateY(60px) skewY(5deg);clip-path:inset(0 0 100% 0);animation:rise .6s var(--d) cubic-bezier(.16,1,.3,1) forwards}}
@keyframes rise{{to{{opacity:1;transform:none;clip-path:inset(-20% 0 -20% 0)}}}}
.bar{{position:absolute;left:0;height:6px;width:0;background:{accent};animation:bar .5s var(--d) cubic-bezier(.16,1,.3,1) forwards}}@keyframes bar{{to{{width:420px}}}}
.dim{{animation:dim .3s var(--d) cubic-bezier(.33,1,.68,1) forwards}}@keyframes dim{{to{{opacity:.55;transform:scale(.92)}}}}"""
    def render(lines):
        out=''
        for l in lines:
            kind,txt,t0,y=l[:4]; dimt=l[4] if len(l)>4 else None
            cls={'s':'s','g':'g slam','i':'i rise'}[kind]
            style=f"top:{y}px;"+(f"--d:{t0}s;" if kind=='i' else '')
            inner=words(txt,t0) if kind=='s' else txt
            if dimt is not None: inner=f'<span class="dim" style="display:inline-block;transform-origin:0 50%;--d:{dimt}s">{inner}</span>'
            out+=f'<div class="ln {cls}" style="{style}">{inner}</div>'
        return out
    return f'<style>{css}</style><div class="cam"><div class="stage"><div class="A"><div class="Ao">{render(A_lines)}</div></div><div class="B">{render(B_lines)}</div></div></div>'
