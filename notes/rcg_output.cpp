// Notes on how to parse *.rcg files
// 
// Relevant files:
//   rcssserver-15.3.0/src/dispsender.cpp
//   rcssserver-15.3.0/src/serializermonitor.cpp


void
DispSenderLoggerV4::sendShow()
{
    serializer().serializeShowBegin( transport(),
                                     stadium().time() );
    // os << "(show " << time;

    serializer().serializeBall( transport(),
                                stadium().ball() );
    // os << " (" << BALL_NAME_SHORT
    //    << ' ' << Quantize( ball.pos().x, PREC )
    //    << ' ' << Quantize( ball.pos().y, PREC )
    //    << ' ' << Quantize( ball.vel().x, PREC )
    //    << ' ' << Quantize( ball.vel().y, PREC )
    //    << ')';

    const Stadium::PlayerCont::const_iterator end = stadium().players().end();
    for ( Stadium::PlayerCont::const_iterator p = stadium().players().begin();
          p != end;
          ++p )
    {
        serializer().serializePlayerBegin( transport(), **p );
    // os << " ("
    //    << '(' << SideStr( player.side() ) << ' ' << player.unum() << ')'
    //    << ' ' << player.playerTypeId()
    //    << ' ' << std::hex << std::showbase
    //    << player.state()
    //    << std::dec << std::noshowbase;
        serializer().serializePlayerPos( transport(), **p );
    // os << ' ' << Quantize( player.pos().x, PREC )
    //    << ' ' << Quantize( player.pos().y, PREC )
    //    << ' ' << Quantize( player.vel().x, PREC )
    //    << ' ' << Quantize( player.vel().y, PREC )
    //    << ' ' << Quantize( Rad2Deg( player.angleBodyCommitted() ), DPREC )
    //    << ' ' << Quantize( Rad2Deg( player.angleNeckCommitted() ), DPREC );
        serializer().serializePlayerArm( transport(), **p );
    // if ( player.arm().isPointing() )
    // {
    //     os << ' ' << Quantize( player.arm().dest().getX(), PREC )
    //        << ' ' << Quantize( player.arm().dest().getY(), PREC );
    // }
        serializer().serializePlayerViewMode( transport(), **p );
    // os << " (v "
    //    << ( player.highQuality() ? "h " : "l " )
    //    << Quantize( Rad2Deg( player.visibleAngle() ), DPREC ) << ')';
        serializer().serializePlayerStamina( transport(), **p );
    // os << " (s "
    //    << player.stamina() << ' '
    //    << player.effort() << ' '
    //    << player.recovery() << ' '
    //    << player.staminaCapacity() << ')';
        serializer().serializePlayerFocus( transport(), **p );
    // if ( player.isEnabled()
    //      && player.getFocusTarget() != NULL )
    // {
    //     os << " (f "
    //        << SideStr( player.getFocusTarget()->side() ) << ' '
    //        << player.getFocusTarget()->unum() << ')';
    // }
        serializer().serializePlayerCounts( transport(), **p );
     // os << " (c "
     //    << player.kickCount() << ' '
     //    << player.dashCount() << ' '
     //    << player.turnCount() << ' '
     //    << player.catchCount() << ' '
     //    << player.moveCount() << ' '
     //    << player.turnNeckCount() << ' '
     //    << player.changeViewCount() << ' '
     //    << player.sayCount() << ' '
     //    << player.tackleCount() << ' '
     //    << player.arm().getCounter() << ' '
     //    << player.attentiontoCount() << ')';
        serializer().serializePlayerEnd( transport() );
    // os << ')';
    }

    serializer().serializeShowEnd( transport() );
    // os << ')';

    transport() << '\n';
}
